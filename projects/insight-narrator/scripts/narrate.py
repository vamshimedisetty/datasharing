"""
Reads weekly_kpis from the DuckDB warehouse, computes week-over-week deltas
and flags statistical anomalies (all in pandas -- no numbers reach the LLM
that weren't computed here first), then asks Claude to narrate the result
in plain English.

Usage:
    python scripts/narrate.py                # narrate the latest week
    python scripts/narrate.py --week 2017-10-16   # narrate a specific week (replay)
    python scripts/narrate.py --all           # narrate every week in the mart
    python scripts/narrate.py --dry-run       # print the computed metrics, skip the LLM call
"""

import argparse
import os
import sys
from pathlib import Path

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_PATH = PROJECT_ROOT / "warehouse" / "insight_narrator.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "output"

TRAILING_WINDOW = 8  # weeks, for the rolling mean/stdev used to flag anomalies
ANOMALY_Z = 1.5       # |z-score| above this gets flagged

METRICS = [
    "order_count",
    "gross_revenue",
    "avg_order_value",
    "unique_customers",
    "avg_review_score",
    "pct_late_deliveries",
    "avg_delivery_days",
]


def load_weekly_kpis() -> pd.DataFrame:
    if not WAREHOUSE_PATH.exists():
        sys.exit(
            f"No warehouse found at {WAREHOUSE_PATH}.\n"
            "Run: python scripts/load_raw.py  &&  dbt run --project-dir dbt_project --profiles-dir dbt_project"
        )
    con = duckdb.connect(str(WAREHOUSE_PATH), read_only=True)
    df = con.execute("select * from weekly_kpis order by order_week").df()
    con.close()
    if df.empty:
        sys.exit("weekly_kpis is empty -- did dbt run succeed?")
    return df


def add_deltas_and_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("order_week").reset_index(drop=True)
    for metric in METRICS:
        # clip rather than leave as inf: a metric jumping from a 0 baseline
        # (e.g. 0% late deliveries -> 97%) is a genuine, large anomaly, but
        # inf/-inf reads badly once it hits the prompt text below.
        wow_pct = df[metric].pct_change() * 100
        df[f"{metric}_wow_pct"] = wow_pct.clip(-500, 500)

        rolling_mean = df[metric].shift(1).rolling(TRAILING_WINDOW, min_periods=3).mean()
        rolling_std = df[metric].shift(1).rolling(TRAILING_WINDOW, min_periods=3).std()
        zscore = (df[metric] - rolling_mean) / rolling_std
        df[f"{metric}_zscore"] = zscore.clip(-8, 8)
        df[f"{metric}_is_anomaly"] = df[f"{metric}_zscore"].abs() >= ANOMALY_Z
    return df


def build_payload(df: pd.DataFrame, as_of_week: pd.Timestamp) -> dict:
    row = df[df["order_week"] == as_of_week]
    if row.empty:
        available = ", ".join(d.strftime("%Y-%m-%d") for d in df["order_week"])
        sys.exit(f"No data for week {as_of_week.date()}. Available weeks: {available}")
    row = row.iloc[0]

    metrics = {}
    anomalies = []
    for metric in METRICS:
        metrics[metric] = {
            "value": round(float(row[metric]), 2) if pd.notna(row[metric]) else None,
            "wow_change_pct": round(float(row[f"{metric}_wow_pct"]), 1) if pd.notna(row[f"{metric}_wow_pct"]) else None,
        }
        if bool(row[f"{metric}_is_anomaly"]):
            anomalies.append({
                "metric": metric,
                "value": metrics[metric]["value"],
                "zscore": round(float(row[f"{metric}_zscore"]), 2),
            })

    return {
        "week_of": as_of_week.strftime("%Y-%m-%d"),
        "metrics": metrics,
        "flagged_anomalies": anomalies,
    }


PROMPT_TEMPLATE = """You are a data analyst writing a weekly KPI summary for an e-commerce
business's leadership team. You are given ONLY the JSON metrics below, already
computed from the warehouse -- do not invent, estimate, or adjust any numbers
that aren't in this payload.

Metrics for the week of {week_of} (week-over-week % change in parentheses):
{metrics_lines}

Statistically flagged anomalies this week (|z-score| >= {threshold}, vs trailing
{window}-week average):
{anomalies_lines}

Write a concise summary (150-200 words) with:
1. A one-line headline capturing the week's overall story.
2. The 2-3 most notable metric changes, citing the actual numbers given.
3. If there are flagged anomalies, name them plainly and offer one plausible
   business hypothesis for each (e.g. a promotion, a logistics issue) --
   framed as a hypothesis to check, not a certainty.
4. One concrete, specific suggested next action for the team.

Plain prose, no markdown headers, no bullet points -- write it as something
a person would actually read in a Monday-morning digest email.
"""


def format_metrics_lines(metrics: dict) -> str:
    lines = []
    for name, m in metrics.items():
        change = f"{m['wow_change_pct']:+.1f}%" if m["wow_change_pct"] is not None else "n/a"
        lines.append(f"  - {name}: {m['value']} ({change})")
    return "\n".join(lines)


def format_anomalies_lines(anomalies: list) -> str:
    if not anomalies:
        return "  (none)"
    return "\n".join(
        f"  - {a['metric']} = {a['value']} (z-score {a['zscore']})" for a in anomalies
    )


def call_claude(payload: dict) -> str:
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it in.")

    prompt = PROMPT_TEMPLATE.format(
        week_of=payload["week_of"],
        metrics_lines=format_metrics_lines(payload["metrics"]),
        anomalies_lines=format_anomalies_lines(payload["flagged_anomalies"]),
        threshold=ANOMALY_Z,
        window=TRAILING_WINDOW,
    )

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", help="ISO date (any day in the target week), e.g. 2017-10-16")
    parser.add_argument("--all", action="store_true", help="Narrate every week in the mart")
    parser.add_argument("--dry-run", action="store_true", help="Print computed metrics, skip the LLM call")
    args = parser.parse_args()

    df = add_deltas_and_anomalies(load_weekly_kpis())
    OUTPUT_DIR.mkdir(exist_ok=True)

    if args.all:
        target_weeks = list(df["order_week"])
    elif args.week:
        target_weeks = [pd.Timestamp(args.week).to_period("W-SUN").start_time]
    else:
        target_weeks = [df["order_week"].iloc[-1]]

    for week in target_weeks:
        payload = build_payload(df, week)
        print(f"\n=== Week of {payload['week_of']} ===")
        print(f"metrics:    {payload['metrics']}")
        print(f"anomalies:  {payload['flagged_anomalies']}")

        if args.dry_run:
            continue

        narrative = call_claude(payload)
        print(f"\n--- narrative ---\n{narrative}\n")

        out_path = OUTPUT_DIR / f"insight_{payload['week_of']}.md"
        out_path.write_text(f"# Weekly Insight -- {payload['week_of']}\n\n{narrative}\n")
        print(f"saved -> {out_path}")


if __name__ == "__main__":
    main()
