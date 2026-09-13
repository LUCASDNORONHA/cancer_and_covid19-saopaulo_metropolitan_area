"""Indicadores descritivos e associações exploratórias."""

import pandas as pd

from .config import CANCER_COLUMNS


def coverage_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Resume período e número de observações por município."""
    return (
        data.groupby("city", as_index=False)
        .agg(inicio=("month_year", "min"), fim=("month_year", "max"), meses=("month_year", "nunique"))
        .sort_values("city")
    )


def totals_by_city_and_diagnosis(data: pd.DataFrame) -> pd.DataFrame:
    """Retorna os totais por município e diagnóstico, em formato longo."""
    return (
        data.melt(id_vars="city", value_vars=[*CANCER_COLUMNS, "U07.1"], var_name="diagnosis", value_name="count")
        .groupby(["city", "diagnosis"], as_index=False)["count"]
        .sum()
    )


def monthly_cancer_profile(data: pd.DataFrame) -> pd.DataFrame:
    """Organiza as três séries de câncer para gráficos temporais."""
    return data.melt(
        id_vars=["city", "month_year"], value_vars=CANCER_COLUMNS,
        var_name="diagnosis", value_name="count"
    )


def correlations_with_covid(data: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Calcula correlações mensais entre COVID-19 e cada diagnóstico de câncer.

    Correlação é uma medida descritiva de associação linear/rank; não identifica
    efeito causal da pandemia sobre os diagnósticos.
    """
    rows = []
    for city, group in data.groupby("city"):
        for diagnosis in CANCER_COLUMNS:
            rows.append({
                "city": city,
                "diagnosis": diagnosis,
                "method": method,
                "correlation": group[diagnosis].corr(group["U07.1"], method=method),
                "months": len(group),
            })
    return pd.DataFrame(rows)


def pandemic_period_comparison(data: pd.DataFrame, pandemic_start: str = "2020-03-01") -> pd.DataFrame:
    """Compara médias mensais antes e a partir de março de 2020.

    Não ajusta por sazonalidade, população ou mudanças de acesso/registro; use
    apenas como descrição inicial da série.
    """
    frame = data.copy()
    frame["period"] = frame["month_year"].ge(pd.Timestamp(pandemic_start)).map(
        {False: "Antes da pandemia", True: "Pandemia e pós-início"}
    )
    return (
        frame.melt(id_vars=["city", "period"], value_vars=CANCER_COLUMNS,
                   var_name="diagnosis", value_name="count")
        .groupby(["city", "diagnosis", "period"], as_index=False)["count"]
        .mean()
        .rename(columns={"count": "media_mensal"})
    )

