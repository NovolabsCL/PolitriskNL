# engine/recommendations.py
# Motor de recomendaciones de PolitRisk Pro.
# Genera análisis extensos, explicativos y profesionales.
# ─────────────────────────────────────────────────────────────────

from dataclasses import dataclass, field
from typing      import List, Optional
from engine.scoring   import IRPResult
from engine.financial import EFAResult, format_usd
from config           import SECTORS


@dataclass
class Condition:
    category:     str   # "contractual" | "financial" | "operational"
    text:         str
    rationale:    str   # explicación de por qué se recomienda
    priority:     str   # "obligatoria" | "recomendada"
    triggered_by: str


@dataclass
class RecommendationResult:
    viability:          str
    executive_summary:  str   # párrafo ejecutivo
    political_analysis: str   # análisis dimensión política
    economic_analysis:  str   # análisis dimensión económica
    business_analysis:  str   # análisis dimensión negocios
    social_analysis:    str   # análisis dimensión social
    opportunity_analysis: str # análisis dimensión oportunidad
    conditions:         List[Condition]
    efa_summary:        Optional[str]
    review_schedule:    str
    analyst_notes:      str = ""
    analyst_approved:   bool = False


def generate(
    irp:        IRPResult,
    asset_type: str,
    efa:        Optional[EFAResult] = None,
) -> RecommendationResult:

    score   = irp.irp_score or 0
    dims    = irp.dimensions
    sector  = SECTORS.get(irp.sector, irp.sector)
    country = irp.country

    pol  = dims.get("political")
    eco  = dims.get("economic")
    biz  = dims.get("business")
    soc  = dims.get("social")
    opp  = dims.get("opportunity")

    pol_score = pol.dimension_score if pol else None
    eco_score = eco.dimension_score if eco else None
    biz_score = biz.dimension_score if biz else None
    soc_score = soc.dimension_score if soc else None
    opp_score = opp.dimension_score if opp else None

    conditions = []

    # ── VIABILIDAD ────────────────────────────────────────────────
    viability, executive_summary = _executive_summary(
        score, asset_type, irp.sector, country, pol_score, eco_score, soc_score
    )

    # ── ANÁLISIS POR DIMENSIÓN ────────────────────────────────────
    political_analysis  = _political_analysis(country, irp.sector, pol, pol_score)
    economic_analysis   = _economic_analysis(country, irp.sector, eco, eco_score, efa)
    business_analysis   = _business_analysis(country, irp.sector, biz, biz_score)
    social_analysis     = _social_analysis(country, irp.sector, soc, soc_score)
    opportunity_analysis= _opportunity_analysis(country, irp.sector, opp, opp_score)

    # ── CONDICIONES ───────────────────────────────────────────────
    conditions = _generate_conditions(irp, asset_type, efa,
                                      pol_score, eco_score, soc_score)

    # ── EFA SUMMARY ───────────────────────────────────────────────
    efa_summary = _efa_summary(efa, country, irp.sector) if efa else None

    # ── REVISIÓN ──────────────────────────────────────────────────
    review_schedule = _review_schedule(score, irp.sector, country)

    return RecommendationResult(
        viability            = viability,
        executive_summary    = executive_summary,
        political_analysis   = political_analysis,
        economic_analysis    = economic_analysis,
        business_analysis    = business_analysis,
        social_analysis      = social_analysis,
        opportunity_analysis = opportunity_analysis,
        conditions           = conditions,
        efa_summary          = efa_summary,
        review_schedule      = review_schedule,
    )


# ─────────────────────────────────────────────────────────────────
# RESUMEN EJECUTIVO
# ─────────────────────────────────────────────────────────────────

def _executive_summary(score, asset_type, sector, country, pol_score, eco_score, soc_score):

    sector_name = SECTORS.get(sector, sector)

    if score >= 70:
        viability = "VIABLE"
        text = (
            f"El análisis de riesgo político para {country} en el sector de {sector_name} "
            f"arroja un Índice de Riesgo Político (IRP) de {score:.1f} sobre 100, lo que sitúa "
            f"a este mercado dentro del rango de condiciones favorables para la internacionalización. "
            f"El marco institucional presenta solidez suficiente para sostener operaciones de mediano "
            f"y largo plazo, con riesgos manejables mediante la aplicación de medidas de protección estándar. "
        )
        if pol_score and pol_score >= 65:
            text += (
                f"El entorno político-institucional es el principal activo del mercado, con indicadores "
                f"de gobernanza que reflejan estabilidad estructural y predictibilidad regulatoria. "
            )
        if eco_score and eco_score >= 65:
            text += (
                f"Las condiciones macroeconómicas respaldan la decisión de entrada, con fundamentos "
                f"financieros que reducen el riesgo de pérdida de valor por factores sistémicos. "
            )
        text += (
            f"Se recomienda proceder con el plan de entrada documentando adecuadamente las cláusulas "
            f"de protección en todos los instrumentos contractuales, y estableciendo un protocolo "
            f"de monitoreo periódico del entorno político."
        )

    elif score >= 40:
        viability = "CONDICIONADO"
        text = (
            f"El análisis de riesgo político para {country} en el sector de {sector_name} "
            f"arroja un Índice de Riesgo Político (IRP) de {score:.1f} sobre 100, lo que corresponde "
            f"a un perfil de riesgo medio que hace viable el proyecto únicamente bajo condiciones "
            f"específicas de estructuración contractual, financiera y operacional. "
            f"El mercado presenta oportunidades genuinas, pero también vulnerabilidades estructurales "
            f"que deben ser gestionadas activamente antes y durante la operación. "
        )
        if pol_score and pol_score < 55:
            text += (
                f"El entorno político-institucional constituye la principal fuente de incertidumbre, "
                f"con indicadores que reflejan fragilidad en la predictibilidad regulatoria y riesgos "
                f"de cambio unilateral de las condiciones de operación. "
            )
        if soc_score and soc_score < 55:
            text += (
                f"La conflictividad social y los factores reputacionales representan un riesgo "
                f"operacional significativo que requiere una estrategia proactiva de relacionamiento "
                f"con comunidades locales y grupos de interés. "
            )
        text += (
            f"La recomendación es proceder con una estrategia de entrada por fases, comprometiendo "
            f"capital de forma gradual conforme el proyecto demuestre viabilidad operacional y "
            f"el entorno político confirme estabilidad. Todas las condiciones identificadas en este "
            f"informe deben ser implementadas antes del desembolso inicial de capital."
        )

    else:
        viability = "NO VIABLE"
        text = (
            f"El análisis de riesgo político para {country} en el sector de {sector_name} "
            f"arroja un Índice de Riesgo Político (IRP) de {score:.1f} sobre 100, nivel que "
            f"indica condiciones estructuralmente adversas para la internacionalización en las "
            f"circunstancias actuales. Los riesgos político-institucionales, financieros y sociales "
            f"identificados superan los umbrales de tolerancia recomendables para este tipo de activo "
            f"y horizonte de inversión. "
            f"Este análisis no recomienda proceder con el proyecto en su configuración actual. "
            f"Si el cliente opta por avanzar de todas formas, será indispensable implementar una "
            f"estructura de mitigación extraordinaria que incluya garantías soberanas o multilaterales, "
            f"seguro de inversión MIGA, estructura off-shore para activos críticos, y un plan de "
            f"salida claramente definido con umbrales de activación preestablecidos."
        )

    return viability, text


# ─────────────────────────────────────────────────────────────────
# ANÁLISIS POR DIMENSIÓN
# ─────────────────────────────────────────────────────────────────

def _political_analysis(country, sector, pol, pol_score):
    if not pol or pol_score is None:
        return "No hay datos suficientes para elaborar un análisis político detallado."

    score_str = f"{pol_score:.1f}"
    inds      = pol.indicators

    # Extraemos scores individuales clave
    corruption = inds.get("POL_01")
    rule_of_law= inds.get("POL_02")
    stability  = inds.get("POL_03")
    gov_eff    = inds.get("POL_04")
    expropr    = inds.get("POL_10")

    text = f"La dimensión político-institucional obtiene un score de {score_str}/100. "

    if pol_score >= 70:
        text += (
            f"El entorno político de {country} presenta condiciones institucionales sólidas "
            f"que generan un marco predecible para la operación empresarial de largo plazo. "
        )
    elif pol_score >= 50:
        text += (
            f"El entorno político de {country} presenta condiciones institucionales moderadas, "
            f"con fortalezas relevantes pero también vulnerabilidades que requieren atención específica. "
        )
    else:
        text += (
            f"El entorno político de {country} refleja debilidades institucionales significativas "
            f"que generan incertidumbre estructural para los inversores extranjeros. "
        )

    if corruption and corruption.score is not None:
        if corruption.score >= 65:
            text += (
                f"El control de la corrupción muestra niveles aceptables (score {corruption.score:.1f}), "
                f"lo que reduce el riesgo de extracción de rentas por parte de funcionarios públicos "
                f"y facilita la operación en un marco de cumplimiento estándar. "
            )
        else:
            text += (
                f"El control de la corrupción es un área de preocupación (score {corruption.score:.1f}), "
                f"lo que exige protocolos de compliance robustos y una debida diligencia exhaustiva "
                f"en todos los procesos de relacionamiento con el sector público. "
                f"Se recomienda implementar un programa de integridad corporativa desde el inicio "
                f"de las operaciones y documentar todas las interacciones con autoridades. "
            )

    if rule_of_law and rule_of_law.score is not None:
        if rule_of_law.score >= 65:
            text += (
                f"El estado de derecho es robusto (score {rule_of_law.score:.1f}), "
                f"lo que proporciona garantías razonables sobre la ejecución de contratos "
                f"y la resolución de disputas a través de mecanismos judiciales locales. "
            )
        else:
            text += (
                f"El estado de derecho presenta debilidades estructurales (score {rule_of_law.score:.1f}). "
                f"La independencia judicial es limitada y la ejecución de contratos puede ser "
                f"lenta e impredecible. Por esta razón, todos los contratos de importancia "
                f"deben incorporar cláusulas de arbitraje internacional que eviten la jurisdicción "
                f"local para la resolución de disputas. "
            )

    if stability and stability.score is not None:
        if stability.score < 50:
            text += (
                f"La estabilidad política es el indicador de mayor preocupación en esta dimensión "
                f"(score {stability.score:.1f}). El país enfrenta riesgos de desestabilización "
                f"que podrían interrumpir las operaciones o generar cambios abruptos en el marco "
                f"regulatorio del sector. Se recomienda monitorear el ciclo electoral y los "
                f"indicadores de conflictividad política con frecuencia trimestral. "
            )

    if expropr and expropr.score is not None:
        expropr_risk = 100 - expropr.score
        if expropr_risk >= 50:
            text += (
                f"El riesgo de expropiación o renegociación unilateral de contratos es elevado "
                f"para el sector {SECTORS.get(sector, sector)}, lo que constituye la principal "
                f"amenaza para la integridad del capital invertido. "
                f"Es imperativo estructurar el proyecto con mecanismos de protección multilateral "
                f"y asegurar que los contratos estén amparados por tratados bilaterales de inversión vigentes. "
            )

    if sector == "mining":
        text += (
            f"Para el sector minero específicamente, el riesgo regulatorio más relevante es "
            f"la modificación del régimen de concesiones y royalties. El analista debe monitorear "
            f"activamente el debate legislativo en torno a la renta minera y las posiciones "
            f"de los principales partidos respecto a la propiedad de los recursos naturales. "
        )
    elif sector in ("renewable", "infra"):
        text += (
            f"En el sector de infraestructura y energía, el riesgo político se manifiesta "
            f"principalmente a través de renegociaciones tarifarias y cambios en los marcos "
            f"de concesiones públicas. La relación con la contraparte soberana debe estar "
            f"respaldada por mecanismos de garantía internacionales desde el inicio del proyecto. "
        )

    return text


def _economic_analysis(country, sector, eco, eco_score, efa):
    if not eco or eco_score is None:
        return "No hay datos suficientes para elaborar un análisis económico detallado."

    score_str = f"{eco_score:.1f}"
    inds      = eco.indicators

    inflation  = inds.get("ECO_01")
    gdp_growth = inds.get("ECO_02")
    debt       = inds.get("ECO_03")
    rating     = inds.get("ECO_05")
    cds        = inds.get("ECO_06")
    fx_vol     = inds.get("ECO_07")

    text = f"La dimensión económico-financiera obtiene un score de {score_str}/100. "

    if eco_score >= 70:
        text += (
            f"Los fundamentos macroeconómicos de {country} son sólidos y proporcionan "
            f"un contexto favorable para la operación empresarial y la repatriación de utilidades. "
        )
    elif eco_score >= 50:
        text += (
            f"Los fundamentos macroeconómicos de {country} son moderados, con algunos indicadores "
            f"que presentan vulnerabilidades que el inversor debe considerar en su estructuración financiera. "
        )
    else:
        text += (
            f"Los fundamentos macroeconómicos de {country} presentan fragilidades significativas "
            f"que se traducen en riesgos financieros directos para el proyecto. "
        )

    if inflation and inflation.score is not None:
        inf_raw = inflation.raw_value
        if inf_raw and inf_raw > 15:
            text += (
                f"La inflación proyectada de {inf_raw:.1f}% es un factor de riesgo relevante "
                f"que erosiona el poder adquisitivo local y puede afectar los costos operacionales "
                f"denominados en moneda local. Se recomienda indexar los contratos de largo plazo "
                f"en dólares o incluir cláusulas de ajuste por inflación. "
            )
        elif inf_raw and inf_raw <= 5:
            text += (
                f"La inflación proyectada de {inf_raw:.1f}% se mantiene dentro de rangos manejables, "
                f"lo que favorece la planificación financiera de largo plazo. "
            )

    if gdp_growth and gdp_growth.raw_value is not None:
        g = gdp_growth.raw_value
        if g >= 4:
            text += (
                f"El crecimiento del PIB proyectado de {g:.1f}% refleja un ciclo económico expansivo "
                f"que respalda la demanda interna y el potencial de mercado del sector. "
            )
        elif g < 1:
            text += (
                f"El crecimiento del PIB de {g:.1f}% indica un ciclo económico débil que puede "
                f"afectar la demanda interna y reducir el tamaño efectivo del mercado en el corto plazo. "
            )

    if debt and debt.raw_value is not None:
        d = debt.raw_value
        if d > 80:
            text += (
                f"La deuda pública de {d:.1f}% del PIB es elevada y genera vulnerabilidad "
                f"ante shocks externos. Un nivel de deuda de esta magnitud puede derivar en "
                f"presiones fiscales que el gobierno administre mediante aumentos de impuestos "
                f"a la inversión extranjera o restricciones a la repatriación de utilidades. "
            )

    if fx_vol and fx_vol.raw_value is not None:
        vol_pct = fx_vol.raw_value * 100
        if vol_pct > 20:
            text += (
                f"La volatilidad cambiaria de {vol_pct:.1f}% en los últimos doce meses es "
                f"significativa y representa un riesgo directo sobre los flujos de caja del proyecto "
                f"cuando se convierten a la moneda de origen del inversor. "
                f"La implementación de una estrategia de cobertura cambiaria es imperativa para "
                f"proyectos con ingresos en moneda local y deuda o distribución de utilidades en dólares. "
            )
        else:
            text += (
                f"La volatilidad cambiaria de {vol_pct:.1f}% en los últimos doce meses es moderada, "
                f"lo que reduce el riesgo de pérdida de valor por fluctuaciones del tipo de cambio. "
            )

    if efa:
        text += (
            f"La exposición financiera máxima estimada para este proyecto asciende a "
            f"{format_usd(efa.efa_usd)}, equivalente al {efa.efa_pct:.1f}% de la inversión total, "
            f"considerando el factor de riesgo político y la volatilidad cambiaria observada. "
            f"Este parámetro debe ser el referente para definir el nivel de cobertura de seguros "
            f"y los montos de las garantías requeridas. "
        )

    return text


def _business_analysis(country, sector, biz, biz_score):
    if not biz or biz_score is None:
        return "No hay datos suficientes para elaborar un análisis del ambiente de negocios."

    score_str = f"{biz_score:.1f}"
    inds      = biz.indicators

    reg_env = inds.get("BIZ_01")
    hci     = inds.get("BIZ_04")
    lpi     = inds.get("BIZ_05")
    internet= inds.get("BIZ_06")
    trace   = inds.get("BIZ_07")
    tbis    = inds.get("BIZ_08")

    text = f"La dimensión de ambiente de negocios obtiene un score de {score_str}/100. "

    if biz_score >= 70:
        text += (
            f"El entorno regulatorio y operacional de {country} es favorable para el desarrollo "
            f"de negocios en el sector de {SECTORS.get(sector, sector)}, con marcos normativos "
            f"que facilitan la inversión extranjera directa. "
        )
    elif biz_score >= 50:
        text += (
            f"El entorno de negocios en {country} presenta condiciones mixtas: hay áreas que "
            f"facilitan la operación, pero también obstáculos regulatorios y operacionales que "
            f"incrementan los costos de entrada y los tiempos de implementación del proyecto. "
        )
    else:
        text += (
            f"El ambiente de negocios en {country} presenta dificultades estructurales que "
            f"elevan significativamente los costos de entrada y de cumplimiento regulatorio, "
            f"requiriendo una planificación más exhaustiva de los plazos de implementación. "
        )

    if hci and hci.raw_value is not None:
        hci_val = hci.raw_value
        if hci_val >= 0.7:
            text += (
                f"El capital humano disponible es una ventaja competitiva del mercado "
                f"(HCI: {hci_val:.2f}), con una fuerza laboral con niveles de productividad "
                f"potencial que facilitan la implementación de operaciones que requieren "
                f"calificaciones técnicas especializadas. "
            )
        elif hci_val < 0.5:
            text += (
                f"La disponibilidad de capital humano calificado es limitada (HCI: {hci_val:.2f}), "
                f"lo que puede derivar en presiones salariales para perfiles especializados "
                f"y en la necesidad de implementar programas de capacitación local o "
                f"recurrir a expatriados para roles técnicos clave. "
            )

    if lpi and lpi.raw_value is not None:
        lpi_val = lpi.raw_value
        if lpi_val >= 3.5:
            text += (
                f"La infraestructura logística es adecuada (LPI: {lpi_val:.2f}/5.0), "
                f"lo que facilita el movimiento de insumos y productos en el contexto "
                f"del sector analizado. "
            )
        else:
            text += (
                f"La infraestructura logística presenta deficiencias (LPI: {lpi_val:.2f}/5.0) "
                f"que pueden incrementar los costos operacionales y los tiempos de abastecimiento. "
                f"Este factor es especialmente relevante para proyectos de minería e infraestructura "
                f"que dependen de cadenas de suministro complejas. "
            )

    if trace and trace.score is not None:
        trace_risk = trace.raw_value
        if trace_risk and trace_risk > 50:
            text += (
                f"El riesgo de soborno empresarial es elevado según el índice TRACE "
                f"({trace_risk:.0f}/100), lo que exige la implementación de controles "
                f"internos robustos y un programa de compliance anticorrupción que cumpla "
                f"con los estándares de la FCPA (EE.UU.) o el UK Bribery Act, según "
                f"la jurisdicción de origen del inversor. "
            )

    if tbis and tbis.score is not None and tbis.raw_value:
        if tbis.raw_value >= 7:
            text += (
                f"La cobertura de tratados bilaterales de inversión es satisfactoria, "
                f"lo que otorga al inversor protecciones legales adicionales frente a "
                f"acciones gubernamentales arbitrarias, incluyendo acceso a mecanismos "
                f"de arbitraje internacional bajo el marco CIADI o UNCITRAL. "
            )
        else:
            text += (
                f"La cobertura de tratados bilaterales de inversión es limitada entre "
                f"{country} y el país de origen del cliente. Se recomienda verificar "
                f"en la base de datos de UNCTAD Investment Policy Hub si existe un TBI "
                f"vigente y, de no haberlo, estructurar el proyecto a través de una "
                f"jurisdicción que sí tenga TBI con {country}. "
            )

    return text


def _social_analysis(country, sector, soc, soc_score):
    if not soc or soc_score is None:
        return "No hay datos suficientes para elaborar un análisis social y reputacional."

    score_str = f"{soc_score:.1f}"
    inds      = soc.indicators

    cpi       = inds.get("SOC_01")
    conflicts = inds.get("SOC_02")
    gpi       = inds.get("SOC_03")
    rsf       = inds.get("SOC_04")
    esg       = inds.get("SOC_07")
    community = inds.get("SOC_08")

    text = f"La dimensión social y reputacional obtiene un score de {soc_score:.1f}/100. "

    if soc_score >= 70:
        text += (
            f"El entorno social de {country} es relativamente estable y presenta condiciones "
            f"favorables para la operación con una licencia social sólida. "
        )
    elif soc_score >= 50:
        text += (
            f"El entorno social de {country} presenta tensiones que requieren gestión activa "
            f"por parte del inversor, especialmente en materia de relacionamiento comunitario "
            f"y cumplimiento de estándares ESG. "
        )
    else:
        text += (
            f"El entorno social de {country} es complejo y representa uno de los principales "
            f"factores de riesgo operacional para el proyecto. La gestión del relacionamiento "
            f"comunitario y la licencia social deben ser prioridades estratégicas desde el "
            f"inicio de la planificación del proyecto. "
        )

    if cpi and cpi.raw_value is not None:
        cpi_val = cpi.raw_value
        if cpi_val < 40:
            text += (
                f"La percepción de corrupción es alta según el Índice de Transparencia Internacional "
                f"(CPI: {cpi_val:.0f}/100), lo que implica riesgos reputacionales para empresas "
                f"internacionales que operan en el mercado. Una asociación con actores locales "
                f"vinculados a prácticas corruptas puede exponer al inversor a sanciones en "
                f"su jurisdicción de origen. "
            )
        elif cpi_val >= 60:
            text += (
                f"La percepción de corrupción se mantiene en niveles manejables "
                f"(CPI: {cpi_val:.0f}/100), lo que reduce el riesgo reputacional asociado "
                f"a la operación en este mercado. "
            )

    if conflicts and conflicts.raw_value is not None:
        conf_val = conflicts.raw_value
        if conf_val > 100:
            text += (
                f"La conflictividad social registrada por ACLED es elevada "
                f"({conf_val:.0f} eventos en los últimos doce meses), lo que refleja "
                f"un tejido social bajo tensión que puede traducirse en interrupciones "
                f"operacionales, bloqueos de acceso a instalaciones o presiones para "
                f"renegociar acuerdos con comunidades locales. "
            )

    if sector == "mining":
        if community and community.score is not None and community.score < 60:
            text += (
                f"La presión comunitaria es un factor crítico para proyectos mineros en {country}. "
                f"La experiencia reciente en la región indica que la falta de una estrategia "
                f"proactiva de consulta y participación comunitaria es la principal causa "
                f"de paralización de proyectos extractivos. Se recomienda iniciar el proceso "
                f"de consulta previa bajo el Convenio 169 de la OIT con suficiente antelación "
                f"al inicio de operaciones, y asignar recursos específicos para un equipo "
                f"de relacionamiento comunitario con presencia permanente en el área de influencia. "
            )

    if esg and esg.score is not None and esg.raw_value:
        if esg.raw_value > 6:
            text += (
                f"El riesgo ESG sectorial es significativo en este mercado, lo que implica "
                f"una mayor exposición a litigios ambientales, presiones regulatorias y "
                f"escrutinio por parte de inversores institucionales con mandatos de sostenibilidad. "
                f"Para empresas que cotizan en bolsa o que dependen de financiamiento de "
                f"fondos ESG, este factor puede afectar el costo de capital del proyecto. "
            )

    return text


def _opportunity_analysis(country, sector, opp, opp_score):
    if not opp or opp_score is None:
        return "No hay datos suficientes para elaborar un análisis de oportunidad estratégica."

    score_str = f"{opp_score:.1f}"
    inds      = opp.indicators

    gdp_pc  = inds.get("OPP_01")
    growth  = inds.get("OPP_02")
    market  = inds.get("OPP_03")
    ied     = inds.get("OPP_04")
    affinity= inds.get("OPP_05")
    multi   = inds.get("OPP_06")

    text = f"La dimensión de oportunidad estratégica obtiene un score de {opp_score:.1f}/100. "

    if opp_score >= 65:
        text += (
            f"El mercado de {country} presenta oportunidades estratégicas significativas "
            f"para el sector de {SECTORS.get(sector, sector)}, con condiciones que justifican "
            f"la evaluación seria de una estrategia de entrada. "
        )
    elif opp_score >= 45:
        text += (
            f"El mercado de {country} ofrece oportunidades moderadas en el sector de "
            f"{SECTORS.get(sector, sector)}, aunque el potencial de crecimiento requiere "
            f"una estrategia de posicionamiento bien definida para ser capturado efectivamente. "
        )
    else:
        text += (
            f"Las oportunidades estratégicas en {country} son limitadas en el horizonte "
            f"de análisis, lo que debilita el caso de inversión desde la perspectiva "
            f"del potencial de retorno. "
        )

    if growth and growth.raw_value is not None:
        g = growth.raw_value
        if g >= 6:
            text += (
                f"El crecimiento proyectado del sector de {g:.1f}% anual es altamente atractivo "
                f"y posiciona a {country} como un mercado de expansión prioritario en la región. "
                f"Este ritmo de crecimiento supera el promedio regional y sugiere que hay demanda "
                f"insatisfecha que un actor bien posicionado puede capturar. "
            )
        elif g >= 3:
            text += (
                f"El crecimiento proyectado del sector de {g:.1f}% anual es razonable y consistente "
                f"con un mercado en expansión gradual. "
            )
        else:
            text += (
                f"El crecimiento proyectado del sector de {g:.1f}% anual es modesto, "
                f"lo que limita el potencial de generación de valor en el mediano plazo. "
            )

    if market and market.raw_value is not None:
        m = market.raw_value
        text += (
            f"El tamaño estimado del mercado objetivo asciende a USD {m:,.0f} millones, "
            f"lo que proporciona un campo de acción suficiente para una operación escalable. "
        )

    if ied and ied.raw_value is not None and ied.raw_value >= 6:
        text += (
            f"El país ofrece incentivos concretos a la inversión extranjera directa que "
            f"pueden mejorar el retorno efectivo del proyecto, incluyendo beneficios "
            f"tributarios o regímenes especiales para el sector analizado. "
            f"Se recomienda verificar la vigencia y condiciones específicas de estos "
            f"incentivos con un asesor legal local antes de la estructuración final. "
        )

    if affinity and affinity.raw_value is not None:
        aff = affinity.raw_value
        if aff >= 7:
            text += (
                f"La alta afinidad cultural e idiomática con el país de origen del cliente "
                f"reduce la distancia psíquica y facilita el proceso de internacionalización, "
                f"disminuyendo los costos de adaptación y los tiempos de curva de aprendizaje. "
            )
        elif aff < 4:
            text += (
                f"La distancia cultural con el país de origen del cliente es significativa, "
                f"lo que puede incrementar los costos de adaptación y requerir mayor inversión "
                f"en capital humano local para una integración exitosa en el mercado. "
            )

    if multi and multi.raw_value is not None and multi.raw_value >= 6:
        text += (
            f"La disponibilidad de financiamiento multilateral para este tipo de proyectos "
            f"en {country} representa una ventaja adicional, ya que permite reducir la "
            f"exposición de capital propio y mejorar la estructura de riesgo del proyecto "
            f"al incorporar a un organismo multilateral como co-financiador. "
        )

    return text


# ─────────────────────────────────────────────────────────────────
# CONDICIONES
# ─────────────────────────────────────────────────────────────────

def _generate_conditions(irp, asset_type, efa, pol_score, eco_score, soc_score):
    conditions = []
    score = irp.irp_score or 0
    pol   = irp.dimensions.get("political")
    eco   = irp.dimensions.get("economic")
    soc   = irp.dimensions.get("social")

    pol_ind = pol.indicators if pol else {}
    eco_ind = eco.indicators if eco else {}
    soc_ind = soc.indicators if soc else {}

    # ── CONTRACTUALES ─────────────────────────────────────────────

    if score < 70 or (pol_score and pol_score < 65):
        conditions.append(Condition(
            category     = "contractual",
            text         = "Cláusula de arbitraje internacional en todos los contratos (CIADI, CCI o UNCITRAL)",
            rationale    = "El marco judicial local presenta riesgos de independencia y eficiencia que hacen aconsejable resolver disputas ante tribunales arbitrales internacionales.",
            priority     = "obligatoria",
            triggered_by = f"IRP={score:.1f} / Dimensión política={pol_score:.1f}" if pol_score else f"IRP={score:.1f}",
        ))

    debt_ind = eco_ind.get("ECO_03")
    if debt_ind and debt_ind.score and debt_ind.score < 50:
        conditions.append(Condition(
            category     = "contractual",
            text         = "Cláusula de estabilización tributaria vinculada al régimen fiscal vigente al momento de la firma",
            rationale    = "La vulnerabilidad fiscal del país incrementa la probabilidad de reformas impositivas que puedan afectar la rentabilidad del proyecto.",
            priority     = "obligatoria",
            triggered_by = f"Deuda/PIB score={debt_ind.score:.1f}",
        ))

    stab = pol_ind.get("POL_03")
    if stab and stab.score and stab.score < 50:
        conditions.append(Condition(
            category     = "contractual",
            text         = "Cláusula de fuerza mayor política con definición amplia que cubra cambios de gobierno, estados de excepción y conflictos civiles",
            rationale    = "La volatilidad política identificada puede derivar en eventos que interrumpan las operaciones sin que medie incumplimiento de ninguna de las partes.",
            priority     = "obligatoria",
            triggered_by = f"Estabilidad política score={stab.score:.1f}",
        ))

    if irp.sector in ("infra", "renewable"):
        conditions.append(Condition(
            category     = "contractual",
            text         = "Contrato take-or-pay con contraparte soberana o empresa pública que garantice ingresos mínimos",
            rationale    = "Los proyectos de infraestructura y energía requieren certeza de ingresos para viabilizar el financiamiento de largo plazo.",
            priority     = "obligatoria",
            triggered_by = f"Sector={irp.sector}",
        ))

    # ── FINANCIERAS ───────────────────────────────────────────────

    expropr = pol_ind.get("POL_10")
    if score < 60 or (expropr and expropr.score and expropr.score < 60):
        conditions.append(Condition(
            category     = "financial",
            text         = "Seguro de inversión MIGA o equivalente multilateral contra expropiación, inconvertibilidad y ruptura de contrato",
            rationale    = "El nivel de riesgo político identificado justifica la contratación de un seguro que transfiera el riesgo de pérdida patrimonial por acción gubernamental a un organismo multilateral.",
            priority     = "obligatoria",
            triggered_by = f"IRP={score:.1f}",
        ))

    if efa and efa.fx_volatility and efa.fx_volatility > 0.12:
        prio = "obligatoria" if efa.fx_volatility > 0.25 else "recomendada"
        conditions.append(Condition(
            category     = "financial",
            text         = f"Estrategia de cobertura cambiaria (hedging) mediante contratos forward o opciones — volatilidad observada: {efa.fx_volatility*100:.1f}%",
            rationale    = "La volatilidad cambiaria observada en los últimos doce meses expone los flujos de caja del proyecto a pérdidas significativas en la conversión a moneda de origen.",
            priority     = prio,
            triggered_by = f"Volatilidad cambiaria={efa.fx_volatility*100:.1f}%",
        ))

    if eco_score and eco_score < 55:
        conditions.append(Condition(
            category     = "financial",
            text         = "Cuenta escrow offshore en jurisdicción segura para depósito de utilidades previo a repatriación",
            rationale    = "Las condiciones macroeconómicas identificadas incrementan el riesgo de controles de capital o restricciones a la transferencia de divisas en escenarios de estrés.",
            priority     = "recomendada",
            triggered_by = f"Dimensión económica={eco_score:.1f}",
        ))

    if irp.sector in ("infra", "renewable", "mining"):
        conditions.append(Condition(
            category     = "financial",
            text         = "Explorar financiamiento del BID, IFC/Banco Mundial o CAF para mejorar la estructura de riesgo e incorporar garantías multilaterales",
            rationale    = "La participación de organismos multilaterales como co-financiadores reduce el riesgo de interferencia gubernamental y mejora las condiciones de acceso a capital.",
            priority     = "recomendada",
            triggered_by = f"Sector={irp.sector}",
        ))

    # ── OPERACIONALES ─────────────────────────────────────────────

    if 40 <= score < 65:
        conditions.append(Condition(
            category     = "operational",
            text         = "Estrategia de entrada por fases con inversión piloto en la primera etapa y puntos de revisión antes de escalar",
            rationale    = "El nivel de incertidumbre del entorno aconseja validar la viabilidad operacional con una exposición de capital limitada antes de comprometer la inversión total.",
            priority     = "obligatoria",
            triggered_by = f"IRP={score:.1f}",
        ))

    if score < 60:
        conditions.append(Condition(
            category     = "operational",
            text         = "Plan de salida documentado con umbrales de activación predefinidos (IRP < 35, crisis política sistémica, cambio de régimen de concesiones)",
            rationale    = "La incertidumbre del entorno requiere que el inversor tenga definido con anticipación el protocolo de desinversión y los umbrales que lo activan.",
            priority     = "obligatoria" if score < 50 else "recomendada",
            triggered_by = f"IRP={score:.1f}",
        ))

    conf = soc_ind.get("SOC_02")
    if conf and conf.score and conf.score < 55:
        conditions.append(Condition(
            category     = "operational",
            text         = "Joint venture o acuerdo de asociación estratégica con socio local de reconocida trayectoria en el sector",
            rationale    = "La conflictividad social identificada se mitiga significativamente cuando el proyecto cuenta con un socio local que aporta legitimidad, conocimiento del entorno y redes de relacionamiento.",
            priority     = "recomendada",
            triggered_by = f"Conflictividad social score={conf.score:.1f}",
        ))

    community = soc_ind.get("SOC_08")
    if irp.sector == "mining" and community and community.score and community.score < 65:
        conditions.append(Condition(
            category     = "operational",
            text         = "Proceso formal de consulta previa a comunidades bajo el Convenio 169 de la OIT con inicio mínimo 18 meses antes del arranque de operaciones",
            rationale    = "La presión comunitaria identificada hace del proceso de consulta previa un factor crítico de viabilidad del proyecto, no solo de cumplimiento legal.",
            priority     = "obligatoria",
            triggered_by = f"Presión comunitaria score={community.score:.1f} / Sector minería",
        ))

    return conditions


# ─────────────────────────────────────────────────────────────────
# EFA SUMMARY
# ─────────────────────────────────────────────────────────────────

def _efa_summary(efa, country, sector):
    text = (
        f"Sobre una inversión total de {format_usd(efa.investment_usd)}, "
        f"la Exposición Financiera Ajustada (EFA) — que estima la pérdida máxima probable "
        f"en un escenario de estrés político-cambiario combinado — asciende a "
        f"{format_usd(efa.efa_usd)}, equivalente al {efa.efa_pct:.1f}% del capital invertido. "
        f"Este cálculo incorpora un factor de riesgo político de {efa.risk_factor:.2f} "
        f"(derivado del IRP) y una volatilidad cambiaria de {efa.fx_volatility*100:.1f}% "
        f"observada en los últimos doce meses. "
        f"La EFA debe ser el referente para dimensionar el seguro de inversión, "
        f"los montos de las garantías contractuales y el nivel de cobertura cambiaria requerido. "
    )
    if efa.rar:
        if efa.rar >= 2:
            text += (
                f"El Retorno Ajustado por Riesgo (RAR) de {efa.rar:.2f}x indica que el retorno "
                f"esperado más que duplica la exposición máxima estimada, lo que respalda "
                f"la decisión de inversión desde una perspectiva de riesgo-retorno."
            )
        elif efa.rar >= 1:
            text += (
                f"El Retorno Ajustado por Riesgo (RAR) de {efa.rar:.2f}x indica que el retorno "
                f"esperado supera la exposición máxima estimada, lo que sustenta la viabilidad "
                f"financiera del proyecto bajo condiciones de mitigación adecuadas."
            )
        else:
            text += (
                f"El Retorno Ajustado por Riesgo (RAR) de {efa.rar:.2f}x indica que el retorno "
                f"esperado no compensa suficientemente la exposición al riesgo identificada, "
                f"lo que debilita el caso financiero del proyecto en su configuración actual."
            )
    return text


# ─────────────────────────────────────────────────────────────────
# REVISIÓN
# ─────────────────────────────────────────────────────────────────

def _review_schedule(score, sector, country):
    if score >= 70:
        freq    = "anual"
        detail  = (
            f"En el caso de {country}, se recomienda realizar una revisión completa del "
            f"análisis cada doce meses, coincidiendo con la publicación de los nuevos "
            f"datos del Banco Mundial y el FMI. "
            f"Adicionalmente, se debe actualizar el análisis de forma inmediata ante los "
            f"siguientes eventos: elecciones con cambio de gobierno, reformas constitucionales "
            f"que afecten el régimen de inversión extranjera, crisis económicas con impacto "
            f"en el tipo de cambio superior al 15% en un período de treinta días, "
            f"o cambios significativos en el marco regulatorio del sector."
        )
    elif score >= 55:
        freq    = "semestral"
        detail  = (
            f"El nivel de riesgo identificado para {country} exige una revisión semestral "
            f"del análisis, coincidiendo con las publicaciones del FMI World Economic Outlook "
            f"(abril y octubre). "
            f"Se debe actualizar el análisis de forma inmediata ante: cualquier cambio de "
            f"gobierno o de ministros clave del área económica, huelgas sectoriales de "
            f"duración superior a siete días, cambios en el régimen de royalties o "
            f"concesiones del sector, o deterioro del rating soberano en dos o más notches."
        )
    elif score >= 40:
        freq    = "trimestral"
        detail  = (
            f"El perfil de riesgo de {country} requiere monitoreo trimestral activo. "
            f"Cada revisión debe incluir: actualización de los indicadores de conflictividad "
            f"(ACLED), seguimiento del GPR Index mensual, revisión de prensa especializada "
            f"sobre el sector, y consulta con el socio local o asesor en el país. "
            f"Cualquier evento político relevante — independientemente del calendario — "
            f"debe gatillar una revisión inmediata del análisis."
        )
    else:
        freq    = "mensual"
        detail  = (
            f"El nivel de riesgo crítico de {country} exige un monitoreo mensual continuo "
            f"que incluya seguimiento semanal de indicadores de alerta temprana: "
            f"spread CDS, tipo de cambio, conflictividad ACLED y cobertura de medios "
            f"internacionales. Se recomienda mantener activo el plan de contingencia "
            f"y revisar mensualmente los umbrales de activación del plan de salida."
        )

    return f"Revisión {freq} recomendada. {detail}"


def conditions_by_category(rec: RecommendationResult) -> dict:
    grouped = {"contractual": [], "financial": [], "operational": []}
    for c in rec.conditions:
        grouped[c.category].append(c)
    return grouped
