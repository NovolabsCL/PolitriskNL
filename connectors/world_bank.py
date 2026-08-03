# connectors/world_bank.py
# Siempre baja el dato más reciente disponible para cada indicador.
# Retorna {valor, año} para que el sistema sepa exactamente
# qué año se está usando en cada dato.
# ─────────────────────────────────────────────────────────────────

import time
from typing import Optional, Tuple

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

WB_INDICATORS = {
    "POL_01": "CC.EST",
    "POL_02": "RL.EST",
    "POL_03": "PV.EST",
    "POL_04": "GE.EST",
    "POL_05": "RQ.EST",
    "ECO_04": "FI.RES.TOTL.MO",
    "BIZ_01": "IC.BUS.EASE.XQ",
    "BIZ_02": "IC.PRT.INVS.XQ",
    "BIZ_03": "IC.REG.DURS",
    "BIZ_04": "HD.HCI.OVRL",
    "BIZ_05": "LP.LPI.OVRL.XQ",
    "BIZ_06": "IT.NET.USER.ZS",
    "OPP_01": "NY.GDP.PCAP.CD",
}

HEADERS  = {"User-Agent": "PolitRiskPro/2.0", "Accept": "application/json"}
MAX_YEAR = 2024   # año más reciente a intentar
LOOKBACK = 8      # cuántos años hacia atrás buscar


def _fetch(url: str) -> Optional[dict]:
    if not REQUESTS_AVAILABLE:
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, verify=True)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def fetch_indicator(iso2: str, wb_code: str) -> Tuple[Optional[float], Optional[int]]:
    """
    Baja el dato más reciente disponible para un indicador.
    Retorna (valor, año) o (None, None) si no hay dato.
    """
    year_from = MAX_YEAR - LOOKBACK
    url = (
        f"https://api.worldbank.org/v2/country/{iso2}"
        f"/indicator/{wb_code}"
        f"?format=json&date={year_from}:{MAX_YEAR}"
        f"&per_page={LOOKBACK + 1}"
    )
    data = _fetch(url)
    if not data or len(data) < 2 or not data[1]:
        return None, None

    # Resultados vienen de más reciente a más antiguo
    for entry in data[1]:
        if entry.get("value") is not None:
            return round(float(entry["value"]), 4), int(entry["date"])

    return None, None


def fetch_all(country_iso2: str) -> dict:
    """
    Baja todos los indicadores del Banco Mundial.
    Retorna: {"POL_01": {"value": 0.97, "year": 2023, "source": "World Bank"}, ...}
    """
    results = {}
    for code, wb_code in WB_INDICATORS.items():
        value, year = fetch_indicator(country_iso2, wb_code)
        results[code] = {"value": value, "year": year, "source": "World Bank"}
        time.sleep(0.25)
    return results
