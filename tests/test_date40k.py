"""Example-based tests for pydate40k.Date40k."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from pydate40k import Date40k


def test_known_date() -> None:
    result = Date40k(datetime(1999, 5, 11, 13, 0, 0))
    assert str(result) == "360 999.M2"


def test_str_delegates_to_get_imperial_date() -> None:
    result = Date40k(datetime(1999, 5, 11, 13, 0, 0))
    assert str(result) == result.get_imperial_date()


def test_none_uses_today(frozen_now: datetime) -> None:
    assert str(Date40k(None)) == "510 024.M3"


def test_default_arg_uses_today(frozen_now: datetime) -> None:
    assert str(Date40k()) == "510 024.M3"


def test_datetime_is_stored_unchanged() -> None:
    when = datetime(2010, 3, 15, 9, 0, 0)
    assert Date40k(when).date == when


@pytest.mark.parametrize(
    "value",
    [
        "1999-05-11 13:00:00",
        42,
        3.14,
        date(1999, 5, 11),
        [2024, 7, 4],
    ],
    ids=["str", "int", "float", "date", "list"],
)
def test_invalid_input_raises_type_error(value: object) -> None:
    with pytest.raises(TypeError):
        Date40k(value)  # type: ignore[arg-type]


def test_leap_day_hour_zero() -> None:
    assert str(Date40k(datetime(2000, 2, 29, 0, 0, 0))) == "164 000.M2"


def test_leap_day_hour_twenty_three() -> None:
    assert str(Date40k(datetime(2000, 2, 29, 23, 0, 0))) == "166 000.M2"


# GitHub issue #1: "It would fail for years before 1000" -- the old
# string-slicing formula truncated real digits instead of dropping a
# leading century digit (e.g. year 7 produced an empty imperial_year).
def test_issue_1_year_500() -> None:
    assert str(Date40k(datetime(500, 1, 1, 0, 0, 0))) == "002 500.M1"


def test_issue_1_year_42() -> None:
    assert str(Date40k(datetime(42, 6, 15, 10, 0, 0))) == "455 042.M1"


def test_issue_1_year_7() -> None:
    assert str(Date40k(datetime(7, 1, 1, 0, 0, 0))) == "002 007.M1"


def test_issue_1_year_999() -> None:
    assert str(Date40k(datetime(999, 12, 31, 23, 0, 0))) == "1001 999.M1"


# Millennium boundaries: the old (year + 1000)[:1] formula was off by one
# at every exact multiple of 1000 (found while fixing issue #1).
def test_millennium_boundary_year_1000() -> None:
    assert str(Date40k(datetime(1000, 1, 1, 0, 0, 0))) == "002 000.M1"


def test_millennium_boundary_year_1001() -> None:
    assert str(Date40k(datetime(1001, 1, 1, 0, 0, 0))) == "002 001.M2"


def test_millennium_boundary_year_2000() -> None:
    assert str(Date40k(datetime(2000, 1, 1, 0, 0, 0))) == "002 000.M2"


def test_millennium_boundary_year_2001() -> None:
    assert str(Date40k(datetime(2001, 1, 1, 0, 0, 0))) == "002 001.M3"


def test_year_fraction_can_render_as_four_digits() -> None:
    # Not a bug: year_fraction is zero-padded to a *minimum* of 3 digits.
    assert str(Date40k(datetime(1999, 12, 31, 23, 0, 0))) == "1001 999.M2"


def test_returns_a_string() -> None:
    assert isinstance(Date40k().get_imperial_date(), str)
