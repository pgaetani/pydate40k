"""pydate40k: convert real-world dates into Warhammer 40,000 Imperial Dating System strings."""

from importlib.metadata import version as _version

from pydate40k.date40k import Date40k

__all__ = ["Date40k"]
__version__ = _version("pydate40k")
