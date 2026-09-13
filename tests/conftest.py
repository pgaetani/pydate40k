"""Shared pytest fixtures for the pydate40k test suite."""

from __future__ import annotations

from datetime import datetime

import pytest

from pydate40k import date40k as date40k_module

FIXED_NOW = datetime(2024, 7, 4, 15, 30, 0)  # -> "510 024.M3"


class _FixedDatetime(datetime):
    @classmethod
    def today(cls) -> _FixedDatetime:
        return cls(2024, 7, 4, 15, 30, 0)


@pytest.fixture
def frozen_now(monkeypatch: pytest.MonkeyPatch) -> datetime:
    """Patch datetime.today() as used inside pydate40k.date40k."""
    monkeypatch.setattr(date40k_module, "datetime", _FixedDatetime)
    return FIXED_NOW
