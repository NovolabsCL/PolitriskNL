# engine/normalizers.py
# Funciones de normalización para los 40 indicadores.
# Convierte cualquier valor crudo a una escala 0-100
# donde 100 = mejor condición para invertir.
# ─────────────────────────────────────────────────────────────────


def normalize_wgi(raw: float) -> float:
    """
    Indicadores WGI del Banco Mundial.
    Escala original: -2.5 (peor) a +2.5 (mejor)
    Ejemplos: Suecia +1.9 → 88 | Chile +0.8 → 66 | Venezuela -1.5 → 20
    """
    raw = max(-2.5, min(2.5, raw))
    return round(((raw + 2.5) / 5.0) * 100, 2)


def normalize_range(value: float, min_val: float,
                    max_val: float, inverse: bool = False) -> float:
    """
    Normalización genérica para cualquier rango.
    inverse=True cuando más alto = peor (ej: días para registrar empresa)
    """
    if max_val == min_val:
        return 50.0
    value = max(min_val, min(max_val, value))
    score = ((value - min_val) / (max_val - min_val)) * 100
    return round(100 - score if inverse else score, 2)


def normalize_inflation(pct: float) -> float:
    """
    Inflación anual en %.
    0% → 100 pts | 50% o más → 0 pts
    """
    pct = max(0.0, min(50.0, pct))
    return round((1 - pct / 50.0) * 100, 2)


def normalize_gdp_growth(pct: float) -> float:
    """
    Crecimiento del PIB real en %.
    Rango: -5% (recesión) a +10% (boom)
    """
    pct = max(-5.0, min(10.0, pct))
    return round(((pct + 5.0) / 15.0) * 100, 2)


def normalize_debt_gdp(pct: float) -> float:
    """
    Deuda pública / PIB en %.
    0% → 100 pts | 200% → 0 pts
    """
    pct = max(0.0, min(200.0, pct))
    return round((1 - pct / 200.0) * 100, 2)


def normalize_sovereign_rating(rating: str) -> float:
    """
    Rating soberano S&P a escala 0-100.
    AAA=100 | A=77 | BBB-=59 | BB=50 | B=36 | D=4
    """
    SCORES = {
        "AAA": 22, "AA+": 21, "AA": 20, "AA-": 19,
        "A+":  18, "A":   17, "A-":  16,
        "BBB+":15, "BBB": 14, "BBB-":13,
        "BB+": 12, "BB":  11, "BB-": 10,
        "B+":   9, "B":    8, "B-":   7,
        "CCC+": 6, "CCC":  5, "CCC-": 4,
        "CC":   3, "C":    2, "D":    1, "NR": 0,
    }
    pts = SCORES.get(str(rating).upper().strip(), 0)
    return round((pts / 22) * 100, 2)


def normalize_gpi(gpi: float) -> float:
    """
    Global Peace Index.
    1.0 = más pacífico (mejor) → 100 pts
    5.0 = menos pacífico (peor) → 0 pts
    """
    gpi = max(1.0, min(5.0, gpi))
    return round((1 - (gpi - 1.0) / 4.0) * 100, 2)


def normalize_rsf(rsf: float) -> float:
    """
    RSF Libertad de Prensa.
    0 = máxima libertad → 100 pts
    100 = sin libertad → 0 pts
    """
    rsf = max(0.0, min(100.0, rsf))
    return round((1 - rsf / 100.0) * 100, 2)


def normalize_gpr(gpr: float) -> float:
    """
    Índice de Riesgo Geopolítico (GPR).
    Base 100 = promedio histórico.
    Más alto = más riesgo geopolítico = peor.
    Rango típico: 50 (calma) a 500 (crisis geopolítica severa).
    """
    gpr = max(0.0, min(500.0, gpr))
    return round((1 - gpr / 500.0) * 100, 2)


def normalize_social_conflicts(events: float) -> float:
    """
    Número de eventos de conflictividad social (ACLED) en 12 meses.
    0 eventos → 100 pts | 500+ eventos → 0 pts
    """
    events = max(0.0, min(500.0, events))
    return round((1 - events / 500.0) * 100, 2)


def normalize_manual_risk(value: float, scale: float = 10.0) -> float:
    """
    Para indicadores manuales donde más = peor riesgo.
    0 = sin riesgo → 100 pts | 10 = riesgo máximo → 0 pts
    Usado en: POL_10 (expropiación), SOC_07, SOC_08
    """
    value = max(0.0, min(scale, value))
    return round((1 - value / scale) * 100, 2)


def normalize_manual_opportunity(value: float, scale: float = 10.0) -> float:
    """
    Para indicadores manuales donde más = mejor oportunidad.
    0 = sin oportunidad → 0 pts | 10 = máxima oportunidad → 100 pts
    Usado en: OPP_04, OPP_05, OPP_06, BIZ_08
    """
    value = max(0.0, min(scale, value))
    return round((value / scale) * 100, 2)


# ── MAPA DE FUNCIONES ─────────────────────────────────────────────
# Relaciona el nombre de la función con la función real.
# El catálogo de indicadores (indicators.py) referencia estos nombres.

NORMALIZER_MAP = {
    "normalize_wgi":                normalize_wgi,
    "normalize_range":              normalize_range,
    "normalize_inflation":          normalize_inflation,
    "normalize_gdp_growth":         normalize_gdp_growth,
    "normalize_debt_gdp":           normalize_debt_gdp,
    "normalize_sovereign_rating":   normalize_sovereign_rating,
    "normalize_gpi":                normalize_gpi,
    "normalize_rsf":                normalize_rsf,
    "normalize_gpr":                normalize_gpr,
    "normalize_social_conflicts":   normalize_social_conflicts,
    "normalize_manual_risk":        normalize_manual_risk,
    "normalize_manual_opportunity": normalize_manual_opportunity,
}


def apply(indicator_code: str, raw_value, normalizer_name: str,
          min_val: float = 0.0, max_val: float = 100.0,
          direction: str = "positive") -> float:
    """
    Aplica la función de normalización correcta a un valor crudo.
    Función principal que usa el motor de scoring.

    Args:
        indicator_code  : código del indicador (ej: "POL_01")
        raw_value       : valor crudo de la fuente
        normalizer_name : nombre de la función (del catálogo)
        min_val / max_val: rango para normalize_range
        direction       : "positive" o "negative"

    Returns:
        score normalizado 0-100
    """
    if raw_value is None:
        return None

    fn = NORMALIZER_MAP.get(normalizer_name)
    if fn is None:
        return None

    try:
        # Funciones con argumentos especiales
        if normalizer_name == "normalize_range":
            score = fn(raw_value, min_val, max_val)
            if direction == "negative":
                score = 100 - score
            return score

        elif normalizer_name in ("normalize_manual_risk",
                                  "normalize_manual_opportunity"):
            return fn(raw_value, max_val)

        else:
            return fn(raw_value)

    except Exception:
        return None
