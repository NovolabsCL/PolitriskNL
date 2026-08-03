# main.py
# Punto de entrada de PolitRisk Pro v2.
# El sistema siempre usa el dato más reciente de cada fuente.
# Ejecutar con: python3 main.py
# ─────────────────────────────────────────────────────────────────

from connectors.orchestrator import fetch_automatic_data
from engine.scoring          import ScoringEngine
from engine.financial        import calculate_efa, calculate_rar, format_usd
from engine.recommendations  import generate, conditions_by_category
from config                  import SECTORS

engine = ScoringEngine()


def run_analysis(
    country:    str,
    sector:     str,
    analysis_year: int,          # año de referencia del informe

    # ── DATOS MANUALES ────────────────────────────────────────────
    pol_06_vdem:         float,  # V-Dem EDI 0-1
    pol_07_freedom:      float,  # Freedom House 0-100
    pol_08_ucdp:         float,  # Conflicto UCDP 0-10
    pol_09_gpr:          float,  # GPR Index
    pol_10_expropiacion: float,  # Riesgo expropiación 0-10
    eco_05_rating:       str,    # Rating S&P
    eco_06_cds:          float,  # CDS spread puntos base
    eco_01_inflacion:    float,  # FMI inflación %
    eco_02_pib:          float,  # FMI crecimiento PIB %
    eco_03_deuda:        float,  # FMI deuda/PIB %
    eco_08_cuenta_cte:   float,  # FMI cuenta corriente/PIB %
    biz_07_trace:        float,  # TRACE Bribery 0-100
    biz_08_tbis:         float,  # TBIs 0-10
    soc_01_cpi:          float,  # CPI TI 0-100
    soc_03_gpi:          float,  # GPI 1-5
    soc_04_rsf:          float,  # RSF 0-100
    soc_05_ndgain:       float,  # ND-GAIN 0-100
    soc_06_epi:          float,  # Yale EPI 0-100
    soc_07_esg:          float,  # ESG 0-10
    soc_08_comunidad:    float,  # Presión comunitaria 0-10
    opp_02_crecimiento:  float,  # Crecimiento sector %
    opp_03_mercado:      float,  # Tamaño mercado USD M
    opp_04_ied:          float,  # Incentivos IED 0-10
    opp_05_afinidad:     float,  # Afinidad cultural 0-10
    opp_06_multilateral: float,  # Multilateral 0-10
    asset_type:          str   = "semi_fixed",
    investment_usd:      float = 0,
    expected_return_usd: float = 0,
):
    print(f"\n{'═'*58}")
    print(f"  POLITRISK PRO v2.0")
    print(f"  {country} | {SECTORS.get(sector, sector)} | {analysis_year}")
    print(f"{'═'*58}")

    # 1. Datos automáticos — siempre el más reciente de cada fuente
    auto_data = fetch_automatic_data(country)

    # 2. Datos manuales
    manual_data = {
        "POL_06": pol_06_vdem,
        "POL_07": pol_07_freedom,
        "POL_08": pol_08_ucdp,
        "POL_09": pol_09_gpr,
        "POL_10": pol_10_expropiacion,
        "ECO_01": eco_01_inflacion,
        "ECO_02": eco_02_pib,
        "ECO_03": eco_03_deuda,
        "ECO_05": eco_05_rating,
        "ECO_06": eco_06_cds,
        "ECO_08": eco_08_cuenta_cte,
        "BIZ_07": biz_07_trace,
        "BIZ_08": biz_08_tbis,
        "SOC_01": soc_01_cpi,
        "SOC_03": soc_03_gpi,
        "SOC_04": soc_04_rsf,
        "SOC_05": soc_05_ndgain,
        "SOC_06": soc_06_epi,
        "SOC_07": soc_07_esg,
        "SOC_08": soc_08_comunidad,
        "OPP_02": opp_02_crecimiento,
        "OPP_03": opp_03_mercado,
        "OPP_04": opp_04_ied,
        "OPP_05": opp_05_afinidad,
        "OPP_06": opp_06_multilateral,
    }

    # 3. Scoring
    irp = engine.compute(
        country       = country,
        sector        = sector,
        analysis_year = analysis_year,
        auto_data     = auto_data,
        manual_data   = manual_data,
    )

    # 4. Exposición financiera
    efa = None
    if investment_usd > 0:
        efa = calculate_efa(
            investment_usd = investment_usd,
            irp_score      = irp.irp_score or 50,
            fx_volatility  = auto_data.get("ECO_07", {}).get("value"),
            fx_data        = auto_data,
        )
        if expected_return_usd > 0:
            efa = calculate_rar(efa, expected_return_usd)

    # 5. Recomendación
    rec = generate(irp, asset_type, efa)

    # 6. Reporte en consola
    _print_report(irp, efa, rec)

    return irp, efa, rec


def _print_report(irp, efa, rec):
    LABELS = {
        "viable":            "VIABLE",
        "conditioned":       "CONDICIONADO",
        "not_viable":        "NO VIABLE",
        "insufficient_data": "DATOS INSUFICIENTES",
    }
    SYMBOLS = {
        "viable": "✅", "conditioned": "⚠️ ",
        "not_viable": "🔴", "insufficient_data": "❓",
    }

    print(f"\n{'─'*58}")
    print(f"  RESULTADO")
    print(f"{'─'*58}")
    print(f"  País:      {irp.country}")
    print(f"  Sector:    {SECTORS.get(irp.sector, irp.sector)}")
    print(f"  Año ref.:  {irp.analysis_year}")
    print(f"  Cobertura: {irp.data_coverage_pct:.0f}%")
    print(f"  Calculado: {irp.computed_at}")

    if irp.data_years:
        print(f"\n  Años de datos automáticos utilizados:")
        for code, year in sorted(irp.data_years.items()):
            print(f"    {code:<8} → {year}")

    print(f"\n  {'DIMENSIÓN':<28} {'SCORE':>6}  {'COB.':>5}")
    print(f"  {'─'*45}")
    for dim in irp.dimensions.values():
        score_str = f"{dim.dimension_score:.1f}" if dim.dimension_score else "N/D"
        bar       = "█" * int((dim.dimension_score or 0) / 5) + "░" * (20 - int((dim.dimension_score or 0) / 5))
        print(f"  {dim.name:<28} {score_str:>6}  {dim.coverage_pct:.0f}%   {bar}")

    print(f"\n  {'─'*45}")
    irp_str = f"{irp.irp_score:.1f}" if irp.irp_score else "N/D"
    symbol  = SYMBOLS.get(irp.risk_level, "")
    label   = LABELS.get(irp.risk_level, irp.risk_level)
    print(f"  IRP TOTAL: {irp_str}   {symbol} {label}")

    if efa:
        print(f"\n{'─'*58}")
        print(f"  EXPOSICIÓN FINANCIERA AJUSTADA")
        print(f"{'─'*58}")
        print(f"  Inversión:    {format_usd(efa.investment_usd)}")
        print(f"  Volatilidad:  {efa.fx_volatility*100:.1f}% cambiaria 12m (Yahoo Finance — hoy)")
        print(f"  EFA:          {format_usd(efa.efa_usd)} ({efa.efa_pct:.1f}%)")
        if efa.rar:
            print(f"  RAR:          {efa.rar:.2f} — {efa.rar_interpretation}")

    print(f"\n{'─'*58}")
    print(f"  {rec.viability_summary}")

    grouped = conditions_by_category(rec)
    for cat, name in [("contractual","CONTRACTUALES"),("financial","FINANCIERAS"),("operational","OPERACIONALES")]:
        conds = grouped.get(cat, [])
        if conds:
            print(f"\n  {name}:")
            for c in conds:
                mark = "⚠️ " if c.priority == "obligatoria" else "→ "
                print(f"    {mark}{c.text}")

    print(f"\n  REVISIÓN: {rec.review_schedule}")
    print(f"\n{'═'*58}\n")


# ─────────────────────────────────────────────────────────────────
#  ANÁLISIS DE EJEMPLO
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_analysis(
        country       = "Chile",
        sector        = "mining",
        analysis_year = 2026,       # año del informe — los datos se toman del más reciente disponible

        pol_06_vdem         = 0.79,
        pol_07_freedom      = 93.0,
        pol_08_ucdp         = 1.0,
        pol_09_gpr          = 120.0,
        pol_10_expropiacion = 3.0,
        eco_05_rating       = "A",
        eco_06_cds          = 85.0,
        eco_01_inflacion    = 4.5,
        eco_02_pib          = 2.5,
        eco_03_deuda        = 38.0,
        eco_08_cuenta_cte   = -3.5,
        biz_07_trace        = 32.0,
        biz_08_tbis         = 7.0,
        soc_01_cpi          = 66.0,
        soc_03_gpi          = 1.78,
        soc_04_rsf          = 31.0,
        soc_05_ndgain       = 56.3,
        soc_06_epi          = 51.1,
        soc_07_esg          = 5.0,
        soc_08_comunidad    = 6.0,
        opp_02_crecimiento  = 4.5,
        opp_03_mercado      = 45000,
        opp_04_ied          = 6.5,
        opp_05_afinidad     = 8.5,
        opp_06_multilateral = 7.0,
        asset_type          = "fixed",
        investment_usd      = 10_000_000,
        expected_return_usd = 1_800_000,
    )
