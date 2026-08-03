# engine/scoring.py
# Motor de cálculo del IRP — ahora guarda el año de cada dato.
# ─────────────────────────────────────────────────────────────────

from dataclasses import dataclass, field
from typing      import Dict, Optional
from datetime    import datetime

from config             import SECTOR_WEIGHTS
from data.indicators    import INDICATORS, BY_DIMENSION
from engine.normalizers import apply


DIMENSION_NAMES = {
    "political":   "Político e Institucional",
    "economic":    "Económico y Financiero",
    "business":    "Ambiente de Negocios",
    "social":      "Social y Reputacional",
    "opportunity": "Oportunidad Estratégica",
}


@dataclass
class IndicatorResult:
    code:        str
    name:        str
    raw_value:   Optional[float]
    score:       Optional[float]
    data_year:   Optional[int]    # año del dato (puede diferir del año del análisis)
    source:      str
    update_freq: str
    input_type:  str              # "api" | "manual"


@dataclass
class DimensionResult:
    key:             str
    name:            str
    indicators:      Dict[str, IndicatorResult]
    dimension_score: Optional[float]
    coverage_pct:    float


@dataclass
class IRPResult:
    country:           str
    sector:            str
    analysis_year:     int          # año del análisis (referencia)
    dimensions:        Dict[str, DimensionResult]
    irp_score:         Optional[float]
    risk_level:        str
    computed_at:       str
    data_coverage_pct: float
    data_years:        Dict[str, int]  # {código: año} de cada dato automático


class ScoringEngine:

    def compute(
        self,
        country:     str,
        sector:      str,
        analysis_year: int,
        auto_data:   dict,    # {"POL_01": {"value": x, "year": y}, ...}
        manual_data: dict,    # {"POL_06": valor, ...}
    ) -> IRPResult:

        if sector not in SECTOR_WEIGHTS:
            raise ValueError(
                f"Sector '{sector}' no existe. "
                f"Opciones: {list(SECTOR_WEIGHTS.keys())}"
            )

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Extraemos valores y años del dict de datos automáticos
        auto_values = {}
        auto_years  = {}
        for k, v in auto_data.items():
            if k.startswith("_"):
                continue
            if isinstance(v, dict):
                auto_values[k] = v.get("value")
                auto_years[k]  = v.get("year")
            else:
                auto_values[k] = v   # compatibilidad con formato plano

        # Combinamos: automáticos + manuales (manuales tienen prioridad)
        all_values = {**auto_values, **manual_data}

        # Normalizamos
        indicator_results = self._normalize_all(all_values, auto_years, now)

        # Agrupamos por dimensión
        dimensions = self._group_by_dimension(indicator_results)

        # Score total ponderado
        weights     = SECTOR_WEIGHTS[sector]
        dim_scores  = []
        dim_weights = []

        for dim_key, weight in weights.items():
            dim = dimensions.get(dim_key)
            if dim and dim.dimension_score is not None:
                dim_scores.append(dim.dimension_score * weight)
                dim_weights.append(weight)

        if sum(dim_weights) >= 0.5:
            factor    = sum(dim_weights)
            irp_score = round(sum(dim_scores) / factor, 2)
        else:
            irp_score = None

        risk_level = self._get_risk_level(irp_score)

        all_ind   = list(indicator_results.values())
        with_data = [i for i in all_ind if i.score is not None]
        coverage  = round(len(with_data) / len(all_ind) * 100, 1) if all_ind else 0

        return IRPResult(
            country           = country,
            sector            = sector,
            analysis_year     = analysis_year,
            dimensions        = dimensions,
            irp_score         = irp_score,
            risk_level        = risk_level,
            computed_at       = now,
            data_coverage_pct = coverage,
            data_years        = {k: v for k, v in auto_years.items() if v},
        )

    def _normalize_all(
        self,
        data:       dict,
        auto_years: dict,
        now:        str,
    ) -> Dict[str, IndicatorResult]:

        results = {}
        for ind in INDICATORS:
            raw = data.get(ind.code)

            # Para el rating soberano (string), no convertir a float
            if raw is not None and ind.normalizer != "normalize_sovereign_rating":
                try:
                    raw = float(raw)
                except (ValueError, TypeError):
                    raw = None

            score = apply(
                indicator_code  = ind.code,
                raw_value       = raw,
                normalizer_name = ind.normalizer,
                min_val         = ind.min_val,
                max_val         = ind.max_val,
                direction       = ind.direction,
            )

            # Año del dato: automático si está disponible, "manual" si no
            data_year = auto_years.get(ind.code)

            results[ind.code] = IndicatorResult(
                code        = ind.code,
                name        = ind.name,
                raw_value   = raw,
                score       = score,
                data_year   = data_year,
                source      = ind.source,
                update_freq = ind.update_freq,
                input_type  = ind.input_type,
            )

        return results

    def _group_by_dimension(
        self, indicator_results: Dict[str, IndicatorResult]
    ) -> Dict[str, DimensionResult]:

        dimensions = {}
        for dim_key, dim_name in DIMENSION_NAMES.items():
            dim_indicators = BY_DIMENSION.get(dim_key, [])
            ind_results    = {
                ind.code: indicator_results[ind.code]
                for ind in dim_indicators
                if ind.code in indicator_results
            }
            with_score = [
                r.score for r in ind_results.values()
                if r.score is not None
            ]
            dim_score = (
                round(sum(with_score) / len(with_score), 2)
                if with_score else None
            )
            coverage = (
                round(len(with_score) / len(ind_results) * 100, 1)
                if ind_results else 0
            )
            dimensions[dim_key] = DimensionResult(
                key             = dim_key,
                name            = dim_name,
                indicators      = ind_results,
                dimension_score = dim_score,
                coverage_pct    = coverage,
            )
        return dimensions

    def _get_risk_level(self, score: Optional[float]) -> str:
        if score is None:   return "insufficient_data"
        if score >= 70:     return "viable"
        if score >= 40:     return "conditioned"
        return "not_viable"
