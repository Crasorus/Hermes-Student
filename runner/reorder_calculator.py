"""
Reorder Point Calculator

Calculates minimum (s) and maximum (S) reorder points using a Poisson-approximated
Normal distribution model for pharmaceutical supply chain items.

Usage:
    from reorder_calculator import calculate_reorder_points
    result = calculate_reorder_points(
        weekly_demand=6,
        lead_time_days=2,
        review_period_days=1,
        cycle_service_level=0.99,
        moq=3
    )
    print(result)  # {'min_reorder_point': 5, 'max_reorder_point': 8}
"""

import math
from scipy.stats import norm


def calculate_reorder_points(
    weekly_demand: float,
    lead_time_days: float,
    review_period_days: float,
    cycle_service_level: float,
    moq: int,
    pack_multiple: int = 1,
) -> dict:
    """
    Calculate min (s) and max (S) reorder points using a Poisson-approximated
    Normal distribution model.

    This model is based on safety stock theory where:
    - Demand is approximated as Poisson (std dev = sqrt(mean))
    - Reorder point protects against demand uncertainty during lead time
    - Max reorder point accounts for demand during lead time + review period

    Args:
        weekly_demand: Units demanded per week (must be > 0)
        lead_time_days: Days from order to receipt (must be > 0)
        review_period_days: Days between stock reviews (must be >= 0)
        cycle_service_level: Target cycle service level, e.g. 0.95, 0.99 (must be 0 < CSL < 1)
        moq: Minimum Order Quantity (must be >= 1)
        pack_multiple: Pack size multiple (optional, not used in calculation)

    Returns:
        dict with keys:
            - min_reorder_point (int): Reorder trigger point (s)
            - max_reorder_point (int): Order up-to level (S)

    Raises:
        ValueError: If any input is invalid
    """
    # Validate inputs
    if weekly_demand <= 0:
        raise ValueError(f"weekly_demand must be > 0, got {weekly_demand}")
    if lead_time_days <= 0:
        raise ValueError(f"lead_time_days must be > 0, got {lead_time_days}")
    if review_period_days < 0:
        raise ValueError(f"review_period_days must be >= 0, got {review_period_days}")
    if not (0 < cycle_service_level < 1):
        raise ValueError(
            f"cycle_service_level must be between 0 and 1 (exclusive), got {cycle_service_level}"
        )
    if moq < 1:
        raise ValueError(f"moq must be >= 1, got {moq}")

    # Calculate mean daily demand (weekly / 7 days)
    mean_daily = weekly_demand / 7

    # Lead time statistics (Poisson approximation: var = mean)
    mu_lt = mean_daily * lead_time_days
    sd_lt = math.sqrt(mu_lt)

    # Lead time + review period statistics
    mu_pw = mean_daily * (lead_time_days + review_period_days)
    sd_pw = math.sqrt(mu_pw)

    # Min reorder point: protects against demand during lead time only
    s = math.ceil(norm.ppf(cycle_service_level, loc=mu_lt, scale=sd_lt))

    # Raw max reorder point: protects against demand during lead time + review period
    s_raw = math.ceil(norm.ppf(cycle_service_level, loc=mu_pw, scale=sd_pw))

    # Actual max reorder point: ensure it accounts for MOQ
    S = max(s_raw, s + moq)

    return {
        "min_reorder_point": s,
        "max_reorder_point": S,
    }


if __name__ == "__main__":
    # Example usage with test cases from the Excel workbook
    test_cases = [
        {
            "weekly_demand": 6,
            "lead_time_days": 2,
            "review_period_days": 1,
            "cycle_service_level": 0.99,
            "moq": 3,
            "expected_s": 5,
            "expected_S": 8,
        },
        {
            "weekly_demand": 3,
            "lead_time_days": 2,
            "review_period_days": 1,
            "cycle_service_level": 0.99,
            "moq": 3,
            "expected_s": 4,
            "expected_S": 7,
        },
        {
            "weekly_demand": 2,
            "lead_time_days": 2,
            "review_period_days": 1,
            "cycle_service_level": 0.70,
            "moq": 2,
            "expected_s": 1,
            "expected_S": 3,
        },
        {
            "weekly_demand": 50,
            "lead_time_days": 24,
            "review_period_days": 28,
            "cycle_service_level": 0.75,
            "moq": 1,
            "expected_s": 181,
            "expected_S": 385,
        },
    ]

    print("Testing reorder point calculator...\n")
    all_passed = True

    for i, test in enumerate(test_cases, 1):
        expected_s = test.pop("expected_s")
        expected_S = test.pop("expected_S")

        result = calculate_reorder_points(**test)
        s = result["min_reorder_point"]
        S = result["max_reorder_point"]

        s_match = s == expected_s
        S_match = S == expected_S
        status = "PASS" if (s_match and S_match) else "FAIL"

        print(f"Test {i}: {status}")
        print(f"  Input: W={test['weekly_demand']}, L={test['lead_time_days']}, "
              f"R={test['review_period_days']}, CSL={test['cycle_service_level']}, MOQ={test['moq']}")
        print(f"  Min Reorder Point (s): {s} (expected {expected_s}) {'MATCH' if s_match else 'MISMATCH'}")
        print(f"  Max Reorder Point (S): {S} (expected {expected_S}) {'MATCH' if S_match else 'MISMATCH'}")
        print()

        if not (s_match and S_match):
            all_passed = False

    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")
        exit(1)
