import json
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd


DATA_DIR = Path(__file__).parent / "data"
OUTPUT_PATH = Path(__file__).parent / "alerts.csv"


# Thresholds used to create binary evidence features.
TEMP_THRESHOLD = 85.0
VIBRATION_THRESHOLD = 4.5


def load_data(data_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load machines, events, and failure labels."""
    machines = pd.read_csv(data_dir / "machines.csv")
    events = pd.read_json(data_dir / "events.jsonl", lines=True)
    failures = pd.read_csv(data_dir / "failures.csv")
    return machines, events, failures


def clean_events(events: pd.DataFrame, machines: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sensor events.

    TODO:
    1) Drop exact duplicates.
    2) Convert timestamp to datetime (invalid values become NaT).
    3) Keep only rows whose machine_id exists in machines.csv.
    4) Fill missing temp_c values using the global median temp_c.
    5) Return a cleaned dataframe.
    """
    raise NotImplementedError("Implement clean_events")


def build_features(cleaned_events: pd.DataFrame) -> pd.DataFrame:
    """
    Build machine-level binary features from event data.

    Required output columns:
    - machine_id
    - high_temp
    - high_vibration

    TODO:
    - Group by machine_id.
    - Use max temp_c and max vibration_mm_s per machine.
    - Convert to binary indicators using module thresholds.
    """
    raise NotImplementedError("Implement build_features")


def _laplace_rate(successes: int, total: int) -> float:
    """Return Laplace-smoothed Bernoulli probability with alpha=1."""
    return (successes + 1) / (total + 2)


def estimate_bayes_params(feature_table: pd.DataFrame) -> Dict[str, float]:
    """
    Estimate prior and conditional probabilities from labeled feature data.

    Input columns expected:
    - high_temp
    - high_vibration
    - failed_next_shift

    TODO:
    - Compute P(F)
    - Compute P(high_temp|F), P(high_temp|not_F)
    - Compute P(high_vibration|F), P(high_vibration|not_F)
    - Use _laplace_rate for all Bernoulli rates.
    - Return a dictionary with these keys:
      p_f,
      p_high_temp_given_f,
      p_high_temp_given_not_f,
      p_high_vib_given_f,
      p_high_vib_given_not_f
    """
    raise NotImplementedError("Implement estimate_bayes_params")


def posterior_failure_risk(high_temp: int, high_vibration: int, params: Dict[str, float]) -> float:
    """
    Compute P(F|E1,E2) using Naive Bayes with binary evidence.

    If evidence value is 0, use the complement probability.
    Example: P(E1=0|F) = 1 - P(high_temp=1|F)
    """
    raise NotImplementedError("Implement posterior_failure_risk")


def build_alerts(feature_table: pd.DataFrame, params: Dict[str, float]) -> pd.DataFrame:
    """Score each machine, then sort and return final alert table."""
    alerts = feature_table[["machine_id", "high_temp", "high_vibration"]].copy()

    # TODO: compute posterior_failure_risk for each row.
    # alerts["posterior_failure_risk"] = ...

    # Required sort order for deterministic top-3 checks.
    # 1) posterior_failure_risk descending
    # 2) machine_id ascending
    raise NotImplementedError("Implement build_alerts")


def main() -> None:
    machines, events, failures = load_data(DATA_DIR)

    cleaned_events = clean_events(events, machines)
    features = build_features(cleaned_events)

    feature_table = features.merge(failures, on="machine_id", how="inner")
    params = estimate_bayes_params(feature_table)

    alerts = build_alerts(feature_table, params)

    expected_columns = [
        "machine_id",
        "high_temp",
        "high_vibration",
        "posterior_failure_risk",
    ]
    assert list(alerts.columns) == expected_columns, "Output schema mismatch"
    assert alerts["posterior_failure_risk"].between(0, 1).all(), "Posterior must be in [0,1]"

    alerts.to_csv(OUTPUT_PATH, index=False)

    top3 = alerts.head(3)["machine_id"].tolist()
    print("Top 3 machines by posterior risk:", top3)

    with (DATA_DIR / "expected_top3.json").open("r", encoding="utf-8") as f:
        expected = json.load(f)

    print("Expected top 3 IDs:", expected["top3_machine_ids"])


if __name__ == "__main__":
    main()
