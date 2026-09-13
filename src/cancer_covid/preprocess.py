"""Ponto de entrada para executar o pré-processamento sem Jupyter."""

from .config import PROCESSED_FILE, RAW_DATA_DIR
from .data import build_processed_dataset


def main() -> None:
    data = build_processed_dataset(RAW_DATA_DIR, PROCESSED_FILE)
    print(f"Base tratada gravada em: {PROCESSED_FILE}")
    print(f"Linhas: {len(data)} | Municípios: {data['city'].nunique()}")


if __name__ == "__main__":
    main()

