# data/indicators.py
# Catálogo de los 40 indicadores de PolitRisk Pro v2
# Cada indicador especifica su fuente, frecuencia de actualización,
# método de normalización y dimensión a la que pertenece.
# ─────────────────────────────────────────────────────────────────

from dataclasses import dataclass
from typing import Optional


@dataclass
class Indicator:
    code:          str            # ej: "POL_01"
    name:          str            # nombre legible
    dimension:     str            # political | economic | business | social | opportunity
    source:        str            # nombre de la fuente
    source_url:    str            # URL de referencia
    input_type:    str            # "api" | "manual"
    update_freq:   str            # diaria | semanal | mensual | semestral | anual
    api_key:       Optional[str]  # clave del indicador en la API (si aplica)
    normalizer:    str            # nombre de la función de normalización
    direction:     str            # "positive" (más=mejor) | "negative" (más=peor)
    min_val:       float          # valor mínimo para normalización
    max_val:       float          # valor máximo para normalización
    description:   str            # qué mide y cómo interpretarlo
    sector_notes:  str = ""       # notas específicas por sector


INDICATORS = [

    # ══════════════════════════════════════════════════════════════
    # DIMENSIÓN 1 — POLÍTICO E INSTITUCIONAL (10 indicadores)
    # ══════════════════════════════════════════════════════════════

    Indicator(
        code        = "POL_01",
        name        = "Control de Corrupción",
        dimension   = "political",
        source      = "World Bank — Worldwide Governance Indicators",
        source_url  = "https://info.worldbank.org/governance/wgi/",
        input_type  = "api",
        update_freq = "anual (rezago 18 meses)",
        api_key     = "CC.EST",
        normalizer  = "normalize_wgi",
        direction   = "positive",
        min_val     = -2.5,
        max_val     = 2.5,
        description = (
            "Mide la percepción de hasta qué punto el poder público "
            "se ejerce para beneficio privado, incluyendo corrupción "
            "menor y a gran escala, y la captura del Estado por élites. "
            "Fuente: agregado de 30+ encuestas y evaluaciones de expertos."
        ),
    ),
    Indicator(
        code        = "POL_02",
        name        = "Estado de Derecho",
        dimension   = "political",
        source      = "World Bank — Worldwide Governance Indicators",
        source_url  = "https://info.worldbank.org/governance/wgi/",
        input_type  = "api",
        update_freq = "anual (rezago 18 meses)",
        api_key     = "RL.EST",
        normalizer  = "normalize_wgi",
        direction   = "positive",
        min_val     = -2.5,
        max_val     = 2.5,
        description = (
            "Refleja la confianza en las reglas de la sociedad: "
            "calidad del cumplimiento de contratos, derechos de "
            "propiedad, policía y tribunales, y riesgo de crimen "
            "y violencia."
        ),
    ),
    Indicator(
        code        = "POL_03",
        name        = "Estabilidad Política y Ausencia de Violencia",
        dimension   = "political",
        source      = "World Bank — Worldwide Governance Indicators",
        source_url  = "https://info.worldbank.org/governance/wgi/",
        input_type  = "api",
        update_freq = "anual (rezago 18 meses)",
        api_key     = "PV.EST",
        normalizer  = "normalize_wgi",
        direction   = "positive",
        min_val     = -2.5,
        max_val     = 2.5,
        description = (
            "Probabilidad de que el gobierno sea desestabilizado o "
            "derrocado por medios inconstitucionales o violentos, "
            "incluyendo terrorismo."
        ),
        sector_notes = "Crítico para minería e infraestructura por exposición de activos fijos.",
    ),
    Indicator(
        code        = "POL_04",
        name        = "Efectividad Gubernamental",
        dimension   = "political",
        source      = "World Bank — Worldwide Governance Indicators",
        source_url  = "https://info.worldbank.org/governance/wgi/",
        input_type  = "api",
        update_freq = "anual (rezago 18 meses)",
        api_key     = "GE.EST",
        normalizer  = "normalize_wgi",
        direction   = "positive",
        min_val     = -2.5,
        max_val     = 2.5,
        description = (
            "Calidad de los servicios públicos, la burocracia, "
            "la independencia del servicio civil respecto a presiones "
            "políticas, y credibilidad del compromiso del gobierno "
            "con sus políticas."
        ),
    ),
    Indicator(
        code        = "POL_05",
        name        = "Calidad Regulatoria",
        dimension   = "political",
        source      = "World Bank — Worldwide Governance Indicators",
        source_url  = "https://info.worldbank.org/governance/wgi/",
        input_type  = "api",
        update_freq = "anual (rezago 18 meses)",
        api_key     = "RQ.EST",
        normalizer  = "normalize_wgi",
        direction   = "positive",
        min_val     = -2.5,
        max_val     = 2.5,
        description = (
            "Capacidad del gobierno para formular e implementar "
            "políticas y regulaciones sólidas que permitan y promuevan "
            "el desarrollo del sector privado."
        ),
    ),
    Indicator(
        code        = "POL_06",
        name        = "Índice de Democracia Electoral (EDI)",
        dimension   = "political",
        source      = "V-Dem — Varieties of Democracy (U. de Gotemburgo)",
        source_url  = "https://www.v-dem.net/",
        input_type  = "manual",
        update_freq = "anual (publicado en marzo)",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 1.0,
        description = (
            "Mide hasta qué punto el ideal de democracia electoral "
            "se alcanza en la práctica. Basado en evaluaciones de "
            "más de 3,500 expertos país por país. Escala 0-1. "
            "El indicador más riguroso académicamente para democracia."
        ),
    ),
    Indicator(
        code        = "POL_07",
        name        = "Libertades Civiles y Derechos Políticos",
        dimension   = "political",
        source      = "Freedom House — Freedom in the World",
        source_url  = "https://freedomhouse.org/report/freedom-world",
        input_type  = "manual",
        update_freq = "anual (publicado en febrero)",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Score agregado de derechos políticos (40 pts) y "
            "libertades civiles (60 pts). 100=máxima libertad. "
            "Usado por inversores institucionales como proxy de "
            "riesgo político estructural."
        ),
    ),
    Indicator(
        code        = "POL_08",
        name        = "Conflicto Armado Organizado (UCDP)",
        dimension   = "political",
        source      = "Uppsala Conflict Data Program — U. de Uppsala",
        source_url  = "https://ucdp.uu.se/",
        input_type  = "manual",
        update_freq = "anual",
        api_key     = None,
        normalizer  = "normalize_manual_risk",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación del nivel de conflicto armado organizado "
            "en el país según el estándar UCDP (>25 muertes en "
            "combate por año). Escala 0-10 asignada por el analista "
            "con base en los datos UCDP. 0=sin conflicto, 10=guerra activa."
        ),
    ),
    Indicator(
        code        = "POL_09",
        name        = "Índice de Riesgo Geopolítico (GPR)",
        dimension   = "political",
        source      = "Caldara & Iacoviello — Federal Reserve / Fed Dallas",
        source_url  = "https://www.matteoiacoviello.com/gpr.htm",
        input_type  = "manual",
        update_freq = "mensual",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 500.0,
        description = (
            "Mide la tensión geopolítica global mediante análisis "
            "automatizado de texto en medios internacionales. "
            "Publicado mensualmente por economistas de la Fed. "
            "Base 100 = promedio histórico. Valor actual disponible "
            "en matteoiacoviello.com/gpr.htm"
        ),
    ),
    Indicator(
        code        = "POL_10",
        name        = "Riesgo de Expropiación y Renegociación Unilateral",
        dimension   = "political",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_risk",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación del analista sobre el riesgo de que el "
            "gobierno expropie activos, renegocie contratos de "
            "forma unilateral o cambie el marco legal del sector. "
            "Considera: historial del país, discurso del gobierno "
            "actual, TBIs vigentes y marco constitucional. "
            "Escala 0-10 (0=sin riesgo, 10=riesgo máximo)."
        ),
        sector_notes = "El indicador más importante para minería e infraestructura.",
    ),

    # ══════════════════════════════════════════════════════════════
    # DIMENSIÓN 2 — ECONÓMICO Y FINANCIERO (8 indicadores)
    # ══════════════════════════════════════════════════════════════

    Indicator(
        code        = "ECO_01",
        name        = "Inflación Proyectada",
        dimension   = "economic",
        source      = "FMI — World Economic Outlook",
        source_url  = "https://www.imf.org/en/Publications/WEO",
        input_type  = "api",
        update_freq = "semestral (abril y octubre)",
        api_key     = "PCPIPCH",
        normalizer  = "normalize_inflation",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 50.0,
        description = (
            "Tasa de inflación al consumidor proyectada por el FMI "
            "para el año en curso. Usa proyecciones WEO, que son "
            "más recientes que los datos históricos del BM."
        ),
    ),
    Indicator(
        code        = "ECO_02",
        name        = "Crecimiento del PIB Real Proyectado",
        dimension   = "economic",
        source      = "FMI — World Economic Outlook",
        source_url  = "https://www.imf.org/en/Publications/WEO",
        input_type  = "api",
        update_freq = "semestral (abril y octubre)",
        api_key     = "NGDP_RPCH",
        normalizer  = "normalize_gdp_growth",
        direction   = "positive",
        min_val     = -5.0,
        max_val     = 10.0,
        description = "Crecimiento del PIB real proyectado por el FMI. Rango esperado -5% a +10%.",
    ),
    Indicator(
        code        = "ECO_03",
        name        = "Deuda Pública Bruta / PIB",
        dimension   = "economic",
        source      = "FMI — World Economic Outlook",
        source_url  = "https://www.imf.org/en/Publications/WEO",
        input_type  = "api",
        update_freq = "semestral",
        api_key     = "GGXWDG_NGDP",
        normalizer  = "normalize_debt_gdp",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 200.0,
        description = "Deuda pública bruta consolidada como % del PIB. Menos=mejor.",
    ),
    Indicator(
        code        = "ECO_04",
        name        = "Reservas Internacionales (meses de importación)",
        dimension   = "economic",
        source      = "World Bank",
        source_url  = "https://data.worldbank.org",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "FI.RES.TOTL.MO",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 24.0,
        description = "Meses de importaciones que cubren las reservas internacionales brutas.",
    ),
    Indicator(
        code        = "ECO_05",
        name        = "Calificación Soberana (S&P)",
        dimension   = "economic",
        source      = "S&P Global Ratings / Fitch / Moody's",
        source_url  = "https://www.spglobal.com/ratings",
        input_type  = "manual",
        update_freq = "continuo (monitorear cambios)",
        api_key     = None,
        normalizer  = "normalize_sovereign_rating",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 22.0,
        description = (
            "Rating soberano en escala S&P: AAA(22), AA+(21)... "
            "BB(11)... B(8)... D(1). Buscar en spglobal.com o "
            "fitchratings.com. Usar la escala S&P como referencia."
        ),
    ),
    Indicator(
        code        = "ECO_06",
        name        = "CDS Spread Soberano (puntos base)",
        dimension   = "economic",
        source      = "World Government Bonds",
        source_url  = "http://www.worldgovernmentbonds.com/",
        input_type  = "manual",
        update_freq = "diaria",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 2000.0,
        description = (
            "Credit Default Swap spread a 5 años en puntos base. "
            "Mide lo que el mercado cobra HOY para asegurar deuda "
            "soberana. Es el indicador de riesgo país más actualizado "
            "disponible. 0pb=riesgo mínimo, 2000pb=riesgo máximo. "
            "Buscar en worldgovernmentbonds.com (gratuito)."
        ),
    ),
    Indicator(
        code        = "ECO_07",
        name        = "Volatilidad Cambiaria (12 meses)",
        dimension   = "economic",
        source      = "Yahoo Finance API",
        source_url  = "https://finance.yahoo.com/",
        input_type  = "api",
        update_freq = "diaria",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 1.0,
        description = (
            "Volatilidad del tipo de cambio respecto al USD en los "
            "últimos 12 meses: (Max-Min)/Promedio. "
            "0=moneda estable, 1=fluctuación total. "
            "Clave para calcular la Exposición Financiera Ajustada (EFA)."
        ),
    ),
    Indicator(
        code        = "ECO_08",
        name        = "Balanza de Cuenta Corriente / PIB",
        dimension   = "economic",
        source      = "FMI — World Economic Outlook",
        source_url  = "https://www.imf.org/en/Publications/WEO",
        input_type  = "api",
        update_freq = "semestral",
        api_key     = "BCA_NGDPD",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = -15.0,
        max_val     = 15.0,
        description = (
            "Saldo de la balanza por cuenta corriente como % del PIB. "
            "Déficits persistentes indican dependencia de capital "
            "extranjero y vulnerabilidad ante salidas de capital."
        ),
    ),

    # ══════════════════════════════════════════════════════════════
    # DIMENSIÓN 3 — AMBIENTE DE NEGOCIOS (8 indicadores)
    # ══════════════════════════════════════════════════════════════

    Indicator(
        code        = "BIZ_01",
        name        = "Entorno Regulatorio para Negocios (B-READY)",
        dimension   = "business",
        source      = "World Bank — Business Ready",
        source_url  = "https://www.worldbank.org/en/programs/business-enabling-environment",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "IC.BUS.EASE.XQ",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Sucesor del Doing Business (discontinuado en 2021 "
            "por escándalos de manipulación). Evalúa el entorno "
            "regulatorio para empresas privadas en 10 dimensiones. "
            "Escala 0-100."
        ),
    ),
    Indicator(
        code        = "BIZ_02",
        name        = "Protección de Inversores Minoritarios",
        dimension   = "business",
        source      = "World Bank",
        source_url  = "https://data.worldbank.org",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "IC.PRT.INVS.XQ",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 10.0,
        description = "Grado de protección legal a inversores minoritarios en transacciones. Escala 0-10.",
    ),
    Indicator(
        code        = "BIZ_03",
        name        = "Tiempo para Constituir una Empresa (días)",
        dimension   = "business",
        source      = "World Bank",
        source_url  = "https://data.worldbank.org",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "IC.REG.DURS",
        normalizer  = "normalize_range",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 200.0,
        description = "Días hábiles para completar el registro legal de una empresa. Menos=mejor.",
    ),
    Indicator(
        code        = "BIZ_04",
        name        = "Índice de Capital Humano (HCI)",
        dimension   = "business",
        source      = "World Bank — Human Capital Project",
        source_url  = "https://www.worldbank.org/en/publication/human-capital",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "HD.HCI.OVRL",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 1.0,
        description = (
            "Productividad potencial de un niño nacido hoy dado "
            "el nivel actual de educación y salud del país. "
            "Escala 0-1. Proxy de disponibilidad de talento calificado."
        ),
        sector_notes = "Especialmente relevante para tech y energía renovable.",
    ),
    Indicator(
        code        = "BIZ_05",
        name        = "Desempeño Logístico (LPI)",
        dimension   = "business",
        source      = "World Bank — Logistics Performance Index",
        source_url  = "https://lpi.worldbank.org/",
        input_type  = "api",
        update_freq = "bienal",
        api_key     = "LP.LPI.OVRL.XQ",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 1.0,
        max_val     = 5.0,
        description = "Calidad de infraestructura logística, aduanas y cadena de suministro. Escala 1-5.",
        sector_notes = "Crítico para minería (exportación de commodities) e infraestructura.",
    ),
    Indicator(
        code        = "BIZ_06",
        name        = "Penetración de Internet",
        dimension   = "business",
        source      = "World Bank",
        source_url  = "https://data.worldbank.org",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "IT.NET.USER.ZS",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = "Porcentaje de la población que usa internet. Proxy de digitalización del mercado.",
        sector_notes = "Indicador principal para tech. Complementario en otros sectores.",
    ),
    Indicator(
        code        = "BIZ_07",
        name        = "Riesgo de Soborno Empresarial (TRACE)",
        dimension   = "business",
        source      = "TRACE International — Bribery Risk Matrix",
        source_url  = "https://www.traceinternational.org/trace-matrix",
        input_type  = "manual",
        update_freq = "anual",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Score TRACE de riesgo de soborno para empresas "
            "operando en ese país. Evalúa oportunidades de soborno, "
            "disuasión, transparencia y anticuerpos culturales. "
            "0=sin riesgo, 100=riesgo máximo. Gratuito en traceinternational.org."
        ),
    ),
    Indicator(
        code        = "BIZ_08",
        name        = "Cobertura de TBIs y Acuerdos de Inversión",
        dimension   = "business",
        source      = "Evaluación del analista (UNCTAD Investment Hub)",
        source_url  = "https://investmentpolicy.unctad.org/",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_opportunity",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación de la cobertura de Tratados Bilaterales de "
            "Inversión (TBI/BIT) entre el país destino y el país de "
            "origen del cliente. Considera: existencia del TBI, "
            "cláusulas de arbitraje, acuerdos de libre comercio "
            "vigentes. Verificar en investmentpolicy.unctad.org. "
            "Escala 0-10."
        ),
    ),

    # ══════════════════════════════════════════════════════════════
    # DIMENSIÓN 4 — SOCIAL Y REPUTACIONAL (8 indicadores)
    # ══════════════════════════════════════════════════════════════

    Indicator(
        code        = "SOC_01",
        name        = "Índice de Percepción de Corrupción (CPI)",
        dimension   = "social",
        source      = "Transparency International",
        source_url  = "https://www.transparency.org/en/cpi",
        input_type  = "manual",
        update_freq = "anual (enero)",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Percepción de corrupción del sector público. "
            "100=sector público percibido como muy limpio. "
            "Basado en 13 fuentes de datos de 12 instituciones. "
            "El indicador anticorrupción más citado del mundo."
        ),
    ),
    Indicator(
        code        = "SOC_02",
        name        = "Conflictividad Social y Protestas (ACLED)",
        dimension   = "social",
        source      = "ACLED — Armed Conflict Location & Event Data",
        source_url  = "https://acleddata.com/",
        input_type  = "api",
        update_freq = "semanal",
        api_key     = None,
        normalizer  = "normalize_social_conflicts",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 500.0,
        description = (
            "Número de eventos de conflicto, protesta y disturbio "
            "registrados en los últimos 12 meses según ACLED. "
            "El dataset más riguroso y actualizado para conflictividad. "
            "Requiere registro gratuito en acleddata.com para API key."
        ),
        sector_notes = "Especialmente relevante para minería (conflictos comunitarios).",
    ),
    Indicator(
        code        = "SOC_03",
        name        = "Índice de Paz Global (GPI)",
        dimension   = "social",
        source      = "Institute for Economics and Peace",
        source_url  = "https://www.visionofhumanity.org/maps/",
        input_type  = "manual",
        update_freq = "anual (junio)",
        api_key     = None,
        normalizer  = "normalize_gpi",
        direction   = "negative",
        min_val     = 1.0,
        max_val     = 5.0,
        description = (
            "Mide el nivel de paz en 23 indicadores cuantitativos "
            "y cualitativos: conflictos internos y externos, "
            "seguridad social, militarización. Escala 1-5 "
            "(1=más pacífico). Publicado anualmente en junio."
        ),
    ),
    Indicator(
        code        = "SOC_04",
        name        = "Libertad de Prensa (RSF)",
        dimension   = "social",
        source      = "Reporters Without Borders — Press Freedom Index",
        source_url  = "https://rsf.org/en/index",
        input_type  = "manual",
        update_freq = "anual (mayo)",
        api_key     = None,
        normalizer  = "normalize_rsf",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Libertad de prensa en escala 0-100. "
            "0=máxima libertad (mejor), 100=sin libertad (peor). "
            "Proxy del espacio cívico y de la transparencia informativa "
            "disponible para el inversor."
        ),
    ),
    Indicator(
        code        = "SOC_05",
        name        = "Vulnerabilidad Climática (ND-GAIN)",
        dimension   = "social",
        source      = "Notre Dame Global Adaptation Initiative",
        source_url  = "https://gain.nd.edu/our-work/country-index/",
        input_type  = "manual",
        update_freq = "anual",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Score ND-GAIN: combina vulnerabilidad al cambio climático "
            "y capacidad de adaptación. Mayor score = menos vulnerable "
            "y más preparado. Especialmente relevante para proyectos "
            "de largo plazo (minería, infraestructura)."
        ),
        sector_notes = "Crítico para minería (riesgo hídrico) y energía renovable.",
    ),
    Indicator(
        code        = "SOC_06",
        name        = "Desempeño Ambiental (EPI)",
        dimension   = "social",
        source      = "Yale Environmental Performance Index",
        source_url  = "https://epi.yale.edu/",
        input_type  = "manual",
        update_freq = "bienal",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100.0,
        description = (
            "Desempeño ambiental del país en 40 indicadores "
            "organizados en 11 categorías. Score 0-100. "
            "Publicado por Yale cada dos años. Proxy de la "
            "exposición a regulación ambiental y litigios ESG."
        ),
    ),
    Indicator(
        code        = "SOC_07",
        name        = "Riesgo ESG Sectorial",
        dimension   = "social",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_risk",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación del analista sobre el riesgo ESG específico "
            "del sector en ese país. Considera: estándares laborales, "
            "riesgo ambiental operacional, cumplimiento CSRD/ESRS "
            "para Europa, Convenio 169 OIT para comunidades indígenas. "
            "Escala 0-10."
        ),
    ),
    Indicator(
        code        = "SOC_08",
        name        = "Presión Comunitaria y Licencia Social",
        dimension   = "social",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_risk",
        direction   = "negative",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación de la resistencia de comunidades locales "
            "al proyecto: historial de conflictos con empresas del "
            "sector, organizaciones de oposición activas, requerimientos "
            "de consulta previa (Convenio 169 OIT). Escala 0-10."
        ),
        sector_notes = "El indicador más crítico para minería extractiva.",
    ),

    # ══════════════════════════════════════════════════════════════
    # DIMENSIÓN 5 — OPORTUNIDAD ESTRATÉGICA (6 indicadores)
    # ══════════════════════════════════════════════════════════════

    Indicator(
        code        = "OPP_01",
        name        = "PIB per Cápita (USD corrientes)",
        dimension   = "opportunity",
        source      = "World Bank",
        source_url  = "https://data.worldbank.org",
        input_type  = "api",
        update_freq = "anual",
        api_key     = "NY.GDP.PCAP.CD",
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 500.0,
        max_val     = 80000.0,
        description = "PIB per cápita en USD. Proxy del tamaño y poder adquisitivo del mercado.",
    ),
    Indicator(
        code        = "OPP_02",
        name        = "Crecimiento Proyectado del Sector (%)",
        dimension   = "opportunity",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = -5.0,
        max_val     = 20.0,
        description = (
            "Tasa de crecimiento proyectada del sector específico "
            "en ese país a 3-5 años. Basarse en: informes sectoriales, "
            "CEPAL, bancos de desarrollo, informes de bancos de inversión. "
            "Porcentaje anual."
        ),
    ),
    Indicator(
        code        = "OPP_03",
        name        = "Tamaño del Mercado Objetivo (USD millones)",
        dimension   = "opportunity",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_range",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 100000.0,
        description = (
            "Tamaño estimado del mercado objetivo en USD millones. "
            "Para minería: valor de producción anual del mineral. "
            "Para energía: mercado de generación del país. "
            "Para infra: pipeline de proyectos públicos. "
            "Para tech: mercado digital total addressable."
        ),
    ),
    Indicator(
        code        = "OPP_04",
        name        = "Incentivos a la Inversión Extranjera Directa",
        dimension   = "opportunity",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_opportunity",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Evaluación de incentivos formales a la IED: zonas "
            "económicas especiales, exenciones tributarias, "
            "garantías de estabilidad jurídica, regímenes de "
            "importación preferencial para equipos. Escala 0-10."
        ),
    ),
    Indicator(
        code        = "OPP_05",
        name        = "Afinidad Cultural e Idiomática",
        dimension   = "opportunity",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_opportunity",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Afinidad del país destino con el país de origen del "
            "cliente: idioma compartido, similitud de marcos legales, "
            "diáspora empresarial establecida, vínculos históricos, "
            "distancia psíquica percibida. Escala 0-10."
        ),
    ),
    Indicator(
        code        = "OPP_06",
        name        = "Acceso a Financiamiento Multilateral",
        dimension   = "opportunity",
        source      = "Evaluación del analista",
        source_url  = "",
        input_type  = "manual",
        update_freq = "por encargo",
        api_key     = None,
        normalizer  = "normalize_manual_opportunity",
        direction   = "positive",
        min_val     = 0.0,
        max_val     = 10.0,
        description = (
            "Disponibilidad de financiamiento multilateral para "
            "el proyecto: BID, BM/IFC, CAF, ADB, BERD según región. "
            "Considera si el sector y país son elegibles y si hay "
            "líneas de crédito activas. Escala 0-10."
        ),
        sector_notes = "Especialmente relevante para infraestructura y energía renovable.",
    ),
]

# ── ACCESO RÁPIDO ─────────────────────────────────────────────────
INDICATOR_MAP  = {ind.code: ind for ind in INDICATORS}
BY_DIMENSION   = {}
for ind in INDICATORS:
    BY_DIMENSION.setdefault(ind.dimension, []).append(ind)

API_INDICATORS    = [i for i in INDICATORS if i.input_type == "api"]
MANUAL_INDICATORS = [i for i in INDICATORS if i.input_type == "manual"]
