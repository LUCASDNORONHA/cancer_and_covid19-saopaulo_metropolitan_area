"""Leitura, validação e transformação dos dados mensais."""

from pathlib import Path

import pandas as pd

from .config import CITY_FILES, DISEASE_COLUMNS, PROCESSED_FILE, REQUIRED_COLUMNS


def _validate_columns(frame: pd.DataFrame, source: Path) -> None:
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"{source.name}: colunas ausentes: {sorted(missing)}")


def clean_city_data(path: str | Path, city: str) -> pd.DataFrame:
    """Lê e padroniza um CSV bruto de um município.

    O hífen em ``U07.1`` representa ausência de registro e é convertido em zero.
    A função também falha cedo diante de datas inválidas, duplicidades ou contagens
    negativas, tornando a transformação auditável.
    """
    source = Path(path)
    frame = pd.read_csv(source)
    _validate_columns(frame, source)
    frame = frame.loc[:, REQUIRED_COLUMNS].copy()
    frame["month_year"] = pd.to_datetime(frame["month_year"], format="%m-%Y", errors="raise")

    for column in DISEASE_COLUMNS:
        frame[column] = pd.to_numeric(frame[column].replace("-", 0), errors="raise")

    if frame["month_year"].duplicated().any():
        raise ValueError(f"{source.name}: há meses duplicados.")
    if (frame[DISEASE_COLUMNS] < 0).any().any():
        raise ValueError(f"{source.name}: há contagens negativas.")

    frame["city"] = city
    frame["year"] = frame["month_year"].dt.year
    frame["month"] = frame["month_year"].dt.month
    return frame.sort_values("month_year").reset_index(drop=True)


def build_processed_dataset(raw_dir: str | Path, output_path: str | Path = PROCESSED_FILE) -> pd.DataFrame:
    """Consolida os CSVs brutos e grava a base mensal tratada em CSV."""
    raw_dir = Path(raw_dir)
    frames = [clean_city_data(raw_dir / filename, city) for city, filename in CITY_FILES.items()]
    dataset = pd.concat(frames, ignore_index=True).sort_values(["city", "month_year"])
    dataset["total_cancers"] = dataset[["C34", "C91", "C92"]].sum(axis=1)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(destination, index=False, date_format="%Y-%m-%d")
    return dataset.reset_index(drop=True)


def load_processed_data(path: str | Path = PROCESSED_FILE) -> pd.DataFrame:
    """Carrega a base tratada, garantindo que a coluna temporal seja datetime."""
    dataset = pd.read_csv(path, parse_dates=["month_year"])
    return dataset.sort_values(["city", "month_year"]).reset_index(drop=True)

