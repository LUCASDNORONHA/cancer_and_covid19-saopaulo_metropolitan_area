import pandas as pd

from cancer_covid.data import clean_city_data


def test_clean_city_data_converts_dash_and_adds_time_features(tmp_path):
    source = tmp_path / "city.csv"
    source.write_text("month_year,C34,C91,C92,U07.1\n01-2020,1,2,3,-\n", encoding="utf-8")

    result = clean_city_data(source, "Teste")

    assert result.loc[0, "U07.1"] == 0
    assert result.loc[0, "city"] == "Teste"
    assert result.loc[0, "year"] == 2020
    assert result.loc[0, "month"] == 1
    assert pd.api.types.is_datetime64_any_dtype(result["month_year"])
