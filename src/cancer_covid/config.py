"""Constantes e caminhos do projeto."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_FILE = PROCESSED_DATA_DIR / "cancer_covid_mensal.csv"

DISEASE_COLUMNS = ["C34", "C91", "C92", "U07.1"]
CANCER_COLUMNS = ["C34", "C91", "C92"]
REQUIRED_COLUMNS = ["month_year", *DISEASE_COLUMNS]

CITY_FILES = {
    "Campinas": "cancer_covid_campinas.csv",
    "Guarulhos": "cancer_covid_guarulhos.csv",
    "São Paulo": "cancer_covid_sao_paulo.csv",
}

DIAGNOSIS_LABELS = {
    "C34": "Neoplasia maligna de brônquios e pulmões",
    "C91": "Leucemia linfoide",
    "C92": "Leucemia mieloide",
    "U07.1": "COVID-19, vírus identificado",
}

