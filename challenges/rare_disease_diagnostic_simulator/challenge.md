# Challenge: Disease Diagnostic Simulator

## Problem
A rare disease affects **1%** of the population.
A medical test for it is **95% accurate**:

- If a patient has the disease, they test positive 95% of the time (sensitivity = 0.95)
- If a patient does not have the disease, they test negative 95% of the time (specificity = 0.95)

If a patient tests positive, what is the probability they actually have the disease?

## Goal
Implement a small simulator that computes this probability using Bayes' theorem.

## Requirements
1. Load the challenge parameters from `data/parameters.json`.
2. Implement `posterior_given_positive` in `starter.py`.
3. Print the posterior probability as both a decimal and a percentage.

## Bayes' theorem reference
\[
P(D \mid +) = \frac{P(+ \mid D)\,P(D)}{P(+ \mid D)\,P(D) + P(+ \mid \neg D)\,P(\neg D)}
\]

Where:
- \(P(D)\): prevalence
- \(P(+\mid D)\): sensitivity
- \(P(+\mid \neg D) = 1 - \text{specificity}\)
