# engine/financial.py
# Cálculo de la Exposición Financiera Ajustada (EFA) y
# el Retorno Ajustado por Riesgo (RAR).
#
# Estas métricas convierten el IRP en números que entiende
# directamente el CFO de una empresa.
# ─────────────────────────────────────────────────────────────────

from dataclasses import dataclass
from typing import Optional


@dataclass
class EFAResult:
    """Resultado del análisis de exposición financiera."""

    # Inputs
    investment_usd:    float          # inversión total en USD
    irp_score:         float          # IRP del análisis (0-100)
    fx_volatility:     float          # volatilidad cambiaria (0-1)
    fx_pair:           Optional[str]  # par de divisas (ej: CLPUSD=X)
    fx_current:        Optional[float]# tipo de cambio actual
    fx_min_12m:        Optional[float]# mínimo del año
    fx_max_12m:        Optional[float]# máximo del año
    fx_avg_12m:        Optional[float]# promedio del año

    # Outputs calculados
    risk_factor:       float          # (1 - IRP/100)
    efa_usd:           float          # Exposición Financiera Ajustada
    efa_pct:           float          # EFA como % de la inversión

    # Retorno ajustado (opcional, si el cliente da datos)
    expected_return_usd: Optional[float] = None
    rar:                 Optional[float] = None  # RAR = retorno/EFA
    rar_interpretation:  Optional[str]  = None


def calculate_efa(
    investment_usd: float,
    irp_score:      float,
    fx_volatility:  Optional[float],
    fx_data:        Optional[dict] = None,
) -> EFAResult:
    """
    Calcula la Exposición Financiera Ajustada (EFA).

    Fórmula:
        EFA = Inversión × Volatilidad_cambiaria × (1 - IRP/100)

    Interpretación:
        Es la pérdida máxima estimada en el peor escenario combinado
        de riesgo político y colapso cambiario.

    Args:
        investment_usd : monto total de la inversión en USD
        irp_score      : score IRP del análisis (0-100)
        fx_volatility  : volatilidad cambiaria 12m (0-1), o None
        fx_data        : dict con _fx_current, _fx_range, _fx_pair

    Returns:
        EFAResult con todos los campos calculados
    """
    # Si no hay dato de volatilidad, usamos 0.15 como valor
    # conservador por defecto (15% es la volatilidad promedio
    # de monedas emergentes en períodos estables)
    if fx_volatility is None:
        fx_volatility = 0.15

    risk_factor = round(1 - irp_score / 100, 4)
    efa_usd     = round(investment_usd * fx_volatility * risk_factor, 2)
    efa_pct     = round((efa_usd / investment_usd) * 100, 2) if investment_usd > 0 else 0

    # Datos de tipo de cambio si están disponibles
    fx_pair    = None
    fx_current = None
    fx_min     = None
    fx_max     = None
    fx_avg     = None

    if fx_data:
        fx_pair    = fx_data.get("_fx_pair")
        fx_current = fx_data.get("_fx_current")
        fx_range   = fx_data.get("_fx_range")
        if fx_range:
            fx_min, fx_max, fx_avg = fx_range

    return EFAResult(
        investment_usd = investment_usd,
        irp_score      = irp_score,
        fx_volatility  = fx_volatility,
        fx_pair        = fx_pair,
        fx_current     = fx_current,
        fx_min_12m     = fx_min,
        fx_max_12m     = fx_max,
        fx_avg_12m     = fx_avg,
        risk_factor    = risk_factor,
        efa_usd        = efa_usd,
        efa_pct        = efa_pct,
    )


def calculate_rar(
    efa_result:          EFAResult,
    expected_return_usd: float,
) -> EFAResult:
    """
    Agrega el Retorno Ajustado por Riesgo (RAR) a un EFAResult.

    Fórmula:
        RAR = Retorno_esperado / EFA

    Interpretación:
        RAR > 2.0 → muy favorable (retorno dobla la exposición)
        RAR 1.0-2.0 → favorable
        RAR 0.5-1.0 → marginal (retorno no cubre bien el riesgo)
        RAR < 0.5 → desfavorable

    Args:
        efa_result           : resultado previo de calculate_efa
        expected_return_usd  : retorno anual esperado en USD

    Returns:
        EFAResult actualizado con RAR
    """
    if efa_result.efa_usd == 0:
        rar = None
        interpretation = "No calculable (EFA = 0)"
    else:
        rar = round(expected_return_usd / efa_result.efa_usd, 2)
        if rar >= 2.0:
            interpretation = "MUY FAVORABLE — el retorno más que dobla la exposición al riesgo"
        elif rar >= 1.0:
            interpretation = "FAVORABLE — el retorno supera la exposición al riesgo"
        elif rar >= 0.5:
            interpretation = "MARGINAL — el retorno no compensa suficientemente el riesgo"
        else:
            interpretation = "DESFAVORABLE — la exposición al riesgo supera el retorno esperado"

    efa_result.expected_return_usd = expected_return_usd
    efa_result.rar                 = rar
    efa_result.rar_interpretation  = interpretation

    return efa_result


def format_usd(amount: float) -> str:
    """Formatea un monto en USD de forma legible."""
    if amount >= 1_000_000_000:
        return f"USD {amount/1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"USD {amount/1_000_000:.2f}M"
    if amount >= 1_000:
        return f"USD {amount/1_000:.1f}K"
    return f"USD {amount:.2f}"
