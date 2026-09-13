"""Gráficos consistentes usados pelo notebook de análise."""

import matplotlib.pyplot as plt
import seaborn as sns

from .analysis import monthly_cancer_profile, totals_by_city_and_diagnosis
from .config import DIAGNOSIS_LABELS


def set_theme() -> None:
    sns.set_theme(style="whitegrid", context="notebook")


def plot_cancer_series(data, city: str):
    """Plota as séries mensais de C34, C91 e C92 de um município."""
    profile = monthly_cancer_profile(data.query("city == @city"))
    profile["diagnosis"] = profile["diagnosis"].map(DIAGNOSIS_LABELS)
    figure, axis = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=profile, x="month_year", y="count", hue="diagnosis", marker="o", ax=axis)
    axis.set(title=f"Séries mensais de câncer — {city}", xlabel="Mês", ylabel="Registros")
    figure.autofmt_xdate()
    return axis


def plot_covid_series(data):
    """Plota a série de COVID-19 comparando os três municípios."""
    figure, axis = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=data, x="month_year", y="U07.1", hue="city", marker="o", ax=axis)
    axis.set(title="Registros mensais de COVID-19", xlabel="Mês", ylabel="Registros (U07.1)")
    figure.autofmt_xdate()
    return axis


def plot_totals(data):
    """Compara totais acumulados; útil apenas como descrição, não como taxa."""
    totals = totals_by_city_and_diagnosis(data)
    totals["diagnosis"] = totals["diagnosis"].map(DIAGNOSIS_LABELS)
    figure, axis = plt.subplots(figsize=(12, 6))
    sns.barplot(data=totals, x="city", y="count", hue="diagnosis", ax=axis)
    axis.set(title="Totais acumulados por município e diagnóstico", xlabel="Município", ylabel="Registros")
    return axis

