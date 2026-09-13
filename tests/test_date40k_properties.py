"""Property-based tests for pydate40k.Date40k, using Hypothesis."""

from __future__ import annotations

from datetime import datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pydate40k import Date40k

_MAKR_CONSTANT = 0.11407955
_MIN_DATE = datetime(1, 1, 1, 0, 0, 0)
_MAX_DATE = datetime(9999, 12, 31, 23, 59, 59)


def _oracle(when: datetime) -> str:
    """Independent reimplementation of the fixed formula (not imported from
    the module under test), so equivalence can't pass by tautology."""
    day_of_year = when.timetuple().tm_yday
    year_fraction = int((day_of_year * 24 + when.hour) * _MAKR_CONSTANT)
    imperial_year = when.year % 1000
    millenium = (when.year - 1) // 1000 + 1
    return f"{year_fraction:03} {imperial_year:03}.M{millenium}"


@given(st.datetimes(min_value=_MIN_DATE, max_value=_MAX_DATE))
def test_matches_reference_oracle(when: datetime) -> None:
    assert Date40k(when).get_imperial_date() == _oracle(when)


@given(st.datetimes(min_value=_MIN_DATE, max_value=_MAX_DATE))
def test_output_shape_is_always_wellformed(when: datetime) -> None:
    result = Date40k(when).get_imperial_date()
    year_fraction, _, tail = result.partition(" ")
    assert year_fraction.isdigit() and len(year_fraction) >= 3
    imperial_year, _, millenium = tail.partition(".M")
    assert len(imperial_year) == 3 and imperial_year.isdigit()
    assert millenium.isdigit() and len(millenium) >= 1


@given(
    st.one_of(
        st.integers(),
        st.text(),
        st.floats(allow_nan=False),
        st.dates(),
        st.lists(st.integers()),
    )
)
def test_invalid_types_always_raise_type_error(value: object) -> None:
    with pytest.raises(TypeError):
        Date40k(value)  # type: ignore[arg-type]
