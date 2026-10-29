
import pytest

from scholarship_awards import (
    award_amount,
    is_eligible,
    application_status,
)


# -------------------- award_amount --------------------

def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("other", 90, "low", False)


def test_negative_marks():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


@pytest.mark.parametrize(
    "category, cutoff",
    [("merit", 75), ("sports", 60), ("arts", 65)],
)
def test_at_cutoff_returns_zero(category, cutoff):
    assert award_amount(category, cutoff, "low", False) == 0


def test_merit_renewal_reduces_cutoff():
    assert award_amount("merit", 71, "low", True) == 100


def test_arts_renewal_reduces_cutoff():
    assert award_amount("arts", 61, "low", True) == 100


def test_sports_renewal_does_not_reduce_cutoff():
    assert award_amount("sports", 65, "low", True) == 500


def test_low_income_standard_rate():
    assert award_amount("merit", 80, "low", False) == 500


def test_other_income_standard_rate():
    assert award_amount("merit", 80, "high", False) == 300


def test_low_income_bonus_above_15_marks():
    assert award_amount("merit", 95, "low", False) == 3200


def test_other_income_bonus_above_15_marks():
    assert award_amount("merit", 95, "high", False) == 2000


def test_low_income_renewal_bonus():
    assert award_amount("merit", 91, "low", True) == 3360


def test_other_income_renewal_bonus():
    assert award_amount("merit", 91, "high", True) == 2100


# -------------------- is_eligible --------------------

def test_special_quota_with_two_backlogs():
    assert is_eligible(40, 2, True) is True


def test_special_quota_with_more_than_two_backlogs():
    assert is_eligible(90, 3, True) is False


def test_regular_applicant_low_attendance():
    assert is_eligible(74, 0, False) is False


def test_regular_applicant_exactly_75_attendance():
    assert is_eligible(75, 1, False) is True


def test_regular_applicant_no_backlogs():
    assert is_eligible(90, 0, False) is True


def test_regular_applicant_multiple_backlogs():
    assert is_eligible(90, 2, False) is False


# -------------------- application_status --------------------

@pytest.mark.parametrize(
    "days_left, renewal, paper, expected",
    [
        (20, False, False, "open"),
        (19, False, False, "closing"),
        (4, False, False, "closed"),
        (30, True, False, "open"),
        (29, True, False, "closing"),
        (14, True, False, "closed"),
        (30, False, True, "open"),
        (29, False, True, "closing"),
        (14, False, True, "closed"),
        (40, True, True, "open"),
        (39, True, True, "closing"),
        (24, True, True, "closed"),
    ],
)
def test_application_status(days_left, renewal, paper, expected):
    assert application_status(days_left, renewal, paper) == expected
