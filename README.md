# Câncer e COVID-19 na Região Metropolitana de São Paulo

Análise exploratória de registros mensais de câncer de pulmão (CID-10 C34), leucemia linfoide (C91), leucemia mieloide (C92) e COVID-19 (U07.1) em Campinas, Guarulhos e São Paulo.

O projeto separa dados brutos, transformação reprodutível e comunicação da análise. As conclusões são descritivas: contagens e correlações não demonstram causalidade.

## Estrutura

```text
data/raw/                    CSVs originais
data/processed/              Base consolidada gerada pelo pipeline
notebooks/01_preprocessamento.ipynb
notebooks/02_analise_exploratoria.ipynb
notebooks/archive/           Notebook histórico
src/cancer_covid/            Pipeline, análises e gráficos reutilizáveis
tests/                        Testes automatizados
pyproject.toml               Dependências e configuração do uv
```

## Como executar com uv

Requer Python 3.10 ou superior e [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
uv run python -m cancer_covid.preprocess
uv run jupyter lab
```

`uv sync` cria/atualiza `.venv` e instala as dependências declaradas em `pyproject.toml`. Execute o notebook [01_preprocessamento.ipynb](notebooks/01_preprocessamento.ipynb) como alternativa ao comando de pipeline; ele cria `data/processed/cancer_covid_mensal.csv`. Depois execute [02_analise_exploratoria.ipynb](notebooks/02_analise_exploratoria.ipynb).

## Dados e transformação

Os CSVs em `data/raw/` possuem `month_year`, `C34`, `C91`, `C92` e `U07.1`. O pipeline valida esquema, datas, duplicidades e contagens negativas; converte datas para formato temporal; interpreta `-` em `U07.1` como zero; e acrescenta município, ano, mês e `total_cancers`.

## Roteiro analítico

O notebook de análise responde a estas perguntas:

1. Qual é a cobertura temporal de cada município?
2. Quais diagnósticos concentram mais registros?
3. Quando ocorreram os picos de COVID-19?
4. Como as séries de câncer variaram no tempo?
5. Há associação linear contemporânea entre COVID-19 e os registros de câncer?
6. Como as médias mensais se comparam antes e após março de 2020?

## Limitações

- Os valores são contagens, não taxas ajustadas pela população.
- Correlação temporal não implica causalidade e não controla sazonalidade, acesso ao diagnóstico, subnotificação ou codificação.
- A comparação antes/depois de março de 2020 é descritiva, não uma estimativa causal.

## Testes

```bash
uv run pytest
```

O notebook original está preservado em `notebooks/archive/`; os notebooks numerados e `src/` são o fluxo atual.
