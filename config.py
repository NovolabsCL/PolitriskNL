# config.py
# Configuración global de PolitRisk Pro v2
# ─────────────────────────────────────────

APP_NAME    = "PolitRisk Pro"
APP_VERSION = "2.0"

# Umbrales del Índice de Riesgo Político (IRP)
IRP_THRESHOLDS = {
    "viable":       70,   # IRP >= 70 → VIABLE
    "conditioned":  40,   # IRP >= 40 → CONDICIONADO
                          # IRP <  40 → NO VIABLE
}

# Colores por nivel de riesgo (para dashboard y reportes)
RISK_COLORS = {
    "viable":      "#1E7D5A",   # verde oscuro
    "conditioned": "#C8991A",   # dorado
    "not_viable":  "#A93226",   # rojo oscuro
}

# Paleta corporativa
PALETTE = {
    "navy":        "#1B2A4A",
    "blue":        "#2E5FA3",
    "gold":        "#C8991A",
    "light_gray":  "#F4F6F9",
    "mid_gray":    "#8395A7",
    "dark_gray":   "#2C3E50",
    "white":       "#FFFFFF",
    "green":       "#1E7D5A",
    "red":         "#A93226",
    "orange":      "#C8991A",
}

# Sectores disponibles
SECTORS = {
    "mining":      "Minería Extractiva",
    "renewable":   "Energía Renovable",
    "infra":       "Infraestructura",
    "tech":        "Tecnología & Startups",
}

# Ponderaciones por sector (deben sumar 1.0)
SECTOR_WEIGHTS = {
    "mining": {
        "political":   0.35,
        "economic":    0.25,
        "business":    0.15,
        "social":      0.20,
        "opportunity": 0.05,
    },
    "renewable": {
        "political":   0.30,
        "economic":    0.22,
        "business":    0.18,
        "social":      0.18,
        "opportunity": 0.12,
    },
    "infra": {
        "political":   0.28,
        "economic":    0.22,
        "business":    0.20,
        "social":      0.18,
        "opportunity": 0.12,
    },
    "tech": {
        "political":   0.15,
        "economic":    0.18,
        "business":    0.32,
        "social":      0.10,
        "opportunity": 0.25,
    },
}

# Tipos de activo (para lógica de recomendación)
ASSET_TYPES = {
    "fixed":      "Activo fijo inamovible (mina, planta, puerto)",
    "semi_fixed": "Activo semi-fijo (manufactura, planta energía)",
    "mobile":     "Activo móvil (tech, servicios, retail)",
}
