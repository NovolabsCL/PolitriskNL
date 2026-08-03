# connectors/imf.py
# Siempre baja el dato más reciente del FMI WEO.
# Retorna {valor, año} para trazabilidad completa.
# ─────────────────────────────────────────────────────────────────

import time
from typing import Optional, Tuple

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

IMF_INDICATORS = {
    "ECO_01": "PCPIPCH",
    "ECO_02": "NGDP_RPCH",
    "ECO_03": "GGXWDG_NGDP",
    "ECO_08": "BCA_NGDPD",
}

HEADERS  = {"User-Agent": "PolitRiskPro/2.0", "Accept": "application/json"}
MAX_YEAR = 2024
LOOKBACK = 5


def _fetch(url: str) -> Optional[dict]:
    if not REQUESTS_AVAILABLE:
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, verify=True)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def fetch_indicator(iso2: str, imf_code: str) -> Tuple[Optional[float], Optional[int]]:
    """
    Baja el dato más reciente del FMI para un indicador.
    Retorna (valor, año) o (None, None).
    """
    url  = f"https://www.imf.org/external/datamapper/api/v1/{imf_code}/{iso2}"
    data = _fetch(url)
    if not data:
        return None, None

    valores = (
        data.get("values", {})
            .get(imf_code, {})
            .get(iso2, {})
    )

    # Busca de más reciente a más antiguo
    for y in range(MAX_YEAR, MAX_YEAR - LOOKBACK - 1, -1):
        v = valores.get(str(y))
        if v is not None:
            return round(float(v), 4), y

    return None, None


def fetch_all(country_iso2: str) -> dict:
    """
    Baja todos los indicadores del FMI.
    Retorna: {"ECO_01": {"value": 11.6, "year": 2022, "source": "IMF WEO"}, ...}
    """
    results = {}
    for code, imf_code in IMF_INDICATORS.items():
        value, year = fetch_indicator(country_iso2, imf_code)
        results[code] = {"value": value, "year": year, "source": "IMF WEO"}
        time.sleep(0.3)
    return results
