# Insight Narrator

**Phase 1** of the [AI-driven analytics projects](../../README.md) roadmap.

Turns a week of e-commerce KPI deltas into a plain-English summary and flags
statistical anomalies -- before anyone opens a dashboard. Built on the same
kind of e-commerce KPI funnel and product-analytics work behind the
Experience section of this portfolio, with an AI narration layer on top.

## Why this project, and how it's built

The interesting (and hard) part of "AI-driven analytics" isn't the prose --
it's making sure the LLM never invents a number. So the pipeline is split
into two halves with a hard boundary between them:

1. **Everything numeric is computed in SQL and pandas.** dbt builds a
   `weekly_kpis` mart; a pandas step computes week-over-week % change and a
   rolling z-score per metric to flag statistical anomalies.
2. **Claude only narrates a JSON payload of already-computed numbers.** The
   prompt explicitly forbids inventing or adjusting figures -- its job is
   explanation and hypothesis generation, not arithmetic.

```
Olist CSVs (or bundled synthetic sample)
        |
        v
  scripts/load_raw.py  --------->  DuckDB: raw.*
        |
        v
  dbt run  (staging -> marts) --->  DuckDB: weekly_kpis
        |
        v
  scripts/narrate.py
    - pandas: WoW % change, rolling z-score anomaly flags
    - Claude API: narrates the computed payload only
        |
        v
  output/insight_<week>.md
```

## Setup

```bash
make setup          # creates .venv, installs requirements.txt
cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY (https://console.anthropic.com/)
```

### Option A -- run the demo now, with bundled synthetic data

No Kaggle account needed. Generates a small synthetic dataset shaped exactly
like the real Olist tables, spanning 10 weeks with two deliberate anomalies
(a demand spike, and a logistics/late-delivery problem) for the narrator to
catch.

```bash
make demo           # generates sample data, loads it, runs dbt, prints computed metrics (no API call)
make narrate         # same pipeline, but actually calls Claude and writes output/insight_*.md
```

### Option B -- run it on the real Olist dataset

1. Download the dataset from Kaggle:
   https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Unzip the CSVs into `data/raw/` (same filenames as the Kaggle download --
   `load_raw.py` looks for `data/raw/` before falling back to the sample data).
3. Run the pipeline:

```bash
make load
make dbt-run
make narrate         # or: python scripts/narrate.py --week 2017-11-20   (a real Black Friday week in this dataset)
```

## Useful commands

```bash
python scripts/narrate.py                    # narrate the latest week
python scripts/narrate.py --week 2017-10-16  # narrate one specific week (replay)
python scripts/narrate.py --all              # narrate every week in the mart
python scripts/narrate.py --dry-run          # print computed metrics, skip the Claude call
```

## What's next (Phase 2 / Phase 3)

- **Pipeline Sentinel**: point an agent at dbt's own test failures and
  pipeline run logs instead of business KPIs -- same "compute first, narrate
  second" pattern, applied to data quality.
- **Warehouse Copilot**: replace the fixed `weekly_kpis` mart with a governed
  dbt Semantic Layer so an LLM can answer *arbitrary* metric questions, not
  just narrate one pre-built table.
