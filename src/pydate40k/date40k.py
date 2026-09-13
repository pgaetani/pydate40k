"""Convert a real-world date into a Warhammer 40,000 Imperial Dating System string."""

from __future__ import annotations

from datetime import datetime

_MAKR_CONSTANT = 0.11407955


class Date40k:
    """A real-world date and its Imperial Dating System representation.

    Supports any year in the full Python ``datetime`` range (1-9999).
    Millennium N covers years ``(N-1)*1000 + 1`` through ``N*1000``
    inclusive (e.g. the 2nd millennium is years 1001-2000), matching the
    usual "no year zero" convention. Note ``year_fraction`` is zero-padded
    to a *minimum* of 3 digits, not clamped to a maximum: it renders as 4
    digits on any Dec 31 at 23:xx local time -- this is expected.
    """

    def __init__(self, date: datetime | None = None) -> None:
        """Wrap ``date``, or the current date and time if ``date`` is ``None``.

        Args:
            date: A ``datetime`` instance, or ``None`` to use
                ``datetime.today()``.

        Raises:
            TypeError: If ``date`` is neither a ``datetime`` instance nor
                ``None``. There is no silent fallback for invalid input --
                only ``None`` means "use today".
        """
        if date is None:
            date = datetime.today()
        elif not isinstance(date, datetime):
            raise TypeError(f"date must be a datetime instance or None, not {type(date).__name__}")
        self.date = date

    def get_imperial_date(self) -> str:
        """Return the Imperial Dating System string. The Emperor protects."""
        day_of_year = self.date.timetuple().tm_yday
        year_fraction = int((day_of_year * 24 + self.date.hour) * _MAKR_CONSTANT)
        imperial_year = self.date.year % 1000
        millenium = (self.date.year - 1) // 1000 + 1
        return f"{year_fraction:03} {imperial_year:03}.M{millenium}"

    def __str__(self) -> str:
        return self.get_imperial_date()
