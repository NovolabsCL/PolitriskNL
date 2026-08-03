# connectors/yahoo_finance.py
# Conector a Yahoo Finance para tipos de cambio y volatilidad cambiaria.
# Actualización: diaria.
# No requiere API key.
# ─────────────────────────────────────────────────────────────────

from typing import Optional, Tuple
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False


def fetch_fx_volatility(fx_pair: str) -> Optional[float]:
    """
    Calcula la volatilidad del tipo de cambio en los últimos 12 meses.

    Fórmula: (Máximo - Mínimo) / Promedio del período
    Resultado: valor entre 0 y 1 (ej: 0.22 = 22% de fluctuación)

    Args:
        fx_pair: par de divisas en formato Yahoo Finance
                 Ej: "CLPUSD=X", "BRLUSD=X", "EURUSD=X"

    Returns:
        volatilidad como float (0-1) o None si no hay datos
    """
    if not YF_AVAILABLE:
        return None
    if fx_pair is None:
        return 0.0   # país dolarizado, sin volatilidad cambiaria

    try:
        end   = datetime.today()
        start = end - timedelta(days=365)

        ticker = yf.Ticker(fx_pair)
        hist   = ticker.history(start=start, end=end)

        if hist.empty or len(hist) < 30:
            return None

        prices  = hist["Close"]
        maximo  = float(prices.max())
        minimo  = float(prices.min())
        promedio= float(prices.mean())

        if promedio == 0:
            return None

        volatilidad = (maximo - minimo) / promedio
        return round(volatilidad, 4)

    except Exception:
        return None


def fetch_fx_current(fx_pair: str) -> Optional[float]:
    """
    Obtiene el tipo de cambio actual (precio de cierre más reciente).

    Args:
        fx_pair: par en formato Yahoo Finance (ej: "CLPUSD=X")

    Returns:
        precio actual o None
    """
    if not YF_AVAILABLE or fx_pair is None:
        return None

    try:
        ticker = yf.Ticker(fx_pair)
        hist   = ticker.history(period="5d")
        if hist.empty:
            return None
        return round(float(hist["Close"].iloc[-1]), 6)
    except Exception:
        return None


def fetch_fx_range_12m(fx_pair: str) -> Optional[Tuple[float, float, float]]:
    """
    Retorna (mínimo, máximo, promedio) del tipo de cambio en 12 meses.
    Útil para el análisis de exposición financiera.
    """
    if not YF_AVAILABLE or fx_pair is None:
        return None

    try:
        end   = datetime.today()
        start = end - timedelta(days=365)

        ticker = yf.Ticker(fx_pair)
        hist   = ticker.history(start=start, end=end)

        if hist.empty:
            return None

        prices = hist["Close"]
        return (
            round(float(prices.min()), 6),
            round(float(prices.max()), 6),
            round(float(prices.mean()), 6),
        )
    except Exception:
        return None
