# Challenge: Bayes-Powered Machine Failure Pipeline

## Problem
You are a junior data engineer at Granite Labs.

A factory wants a simple alerting system for machine failures in the next shift.
You are given raw machine metadata, noisy sensor events, and historical labels.

Your job is to build a small data pipeline and compute a Bayesian failure-risk score per machine.

## Goal
Create an `alerts.csv` file ranked by posterior failure risk.

This challenge is intentionally designed to practice both:
- data engineering (ingest, clean, transform, join, output)
- Bayesian statistical analysis (prior, conditional probabilities, posterior)

Target completion time: about 2 hours (novice)

## Files
- `data/machines.csv`
- `data/events.jsonl`
- `data/failures.csv`
- `data/expected_top3.json` (for quick self-check at the end)
- `starter.py`

## Requirements
1. Load all three input datasets.
2. Clean the events dataset:
   - drop exact duplicate rows
   - normalize timestamps to a valid datetime type
   - remove rows with unknown `machine_id`
   - impute missing `temp_c` with the global median temperature
3. Build machine-level binary evidence features:
   - `high_temp = 1` if machine max `temp_c >= 85`, else `0`
   - `high_vibration = 1` if machine max `vibration_mm_s >= 4.5`, else `0`
4. Join features with labels from `failures.csv`.
5. Estimate probabilities using frequency counts with Laplace smoothing (+1):
   - `P(F)` where `F = failed_next_shift = 1`
   - `P(high_temp | F)` and `P(high_temp | not F)`
   - `P(high_vibration | F)` and `P(high_vibration | not F)`
6. Compute posterior risk for each machine using:

\[
P(F \mid E_1, E_2) =
\frac{P(E_1 \mid F)P(E_2 \mid F)P(F)}
{P(E_1 \mid F)P(E_2 \mid F)P(F) + P(E_1 \mid \neg F)P(E_2 \mid \neg F)P(\neg F)}
\]

Where:
- `E1` is observed value of `high_temp` for that machine
- `E2` is observed value of `high_vibration` for that machine

Hint: if `E1 = 0`, use `1 - P(high_temp | F)` (and similarly for other terms).

7. Create `alerts.csv` sorted by:
   - `posterior_failure_risk` descending
   - `machine_id` ascending (tie-break)

The output columns must be exactly:
- `machine_id`
- `high_temp`
- `high_vibration`
- `posterior_failure_risk`

8. Print the top 3 machine IDs in order.

## Constraints
- Use Python and pandas.
- Do not hardcode expected machine IDs or probabilities.
- Implement the pipeline in `starter.py` function-by-function.

## Self-check
After your pipeline runs, compare your printed top-3 IDs to `data/expected_top3.json`.

## Reflection (write 2-4 sentences each)
1. Why can a machine with strong warning signals still have moderate posterior risk?
2. Which cleaning rule had the biggest impact on your output?
3. What is one additional feature you would engineer next?
