import json
from pathlib import Path


def posterior_given_positive(prevalence: float, sensitivity: float, specificity: float) -> float:
    false_positive_rate = 1 - specificity
    numerator = sensitivity * prevalence
    denominator = numerator + false_positive_rate * (1 - prevalence)
    return numerator / denominator


def main() -> None:
    parameters_path = Path(__file__).parent / "data" / "parameters.json"
    with parameters_path.open("r", encoding="utf-8") as file:
        params = json.load(file)

    posterior = posterior_given_positive(
        prevalence=params["prevalence"],
        sensitivity=params["sensitivity"],
        specificity=params["specificity"],
    )

    print(f"P(disease | positive) = {posterior:.6f}")
    print(f"P(disease | positive) = {posterior * 100:.2f}%")


if __name__ == "__main__":
    main()
