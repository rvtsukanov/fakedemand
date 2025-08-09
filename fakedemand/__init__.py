"""
Fakedemand package for generating synthetic demand data.

This package provides various factors for creating realistic demand patterns
including trends, seasonality, change points, and more.
"""

from .core import Factor
from .series import Row
from .factors import (
    OOS,
    LinearTrend,
    ChangePoints,
    Seasonality,
    NewTrend,
    Sales,
    Constant,
    Multiplier
)

__all__ = [
    'Factor',
    'Row',
    'OOS',
    'LinearTrend',
    'ChangePoints',
    'Seasonality',
    'NewTrend',
    'Sales',
    'Constant',
    'Multiplier'
]
