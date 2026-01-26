"""
Unit tests for utils.py
"""

import pytest

from stroke_ward_model.utils import minutes_to_ampm


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (0, "12:00 AM"),
        (60, "1:00 AM"),
        (11 * 60 + 59, "11:59 AM"),
        (12 * 60, "12:00 PM"),
        (13 * 60 + 5, "1:05 PM"),
        (23 * 60 + 59, "11:59 PM"),
        (24 * 60, "12:00 AM"),
        (24 * 60 + 75, "1:15 AM")
    ],
)
def test_minutes_to_ampm(minutes, expected):
    """minutes_to_ampm should convert minutes into H:MM AM/PM format."""
    assert minutes_to_ampm(minutes) == expected
