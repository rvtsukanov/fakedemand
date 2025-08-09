"""
Factors package for fakedemand.

This package contains all the factor classes that can be used to generate
synthetic demand data with various patterns and seasonality.
"""

from .oos import OOS
from .linear_trend import LinearTrend
from .change_points import ChangePoints
from .seasonality import Seasonality
from .new_trend import NewTrend
from .sales import Sales
from .constant import Constant, Multiplier
from .promo import Promo
from .noise import Noise

__all__ = [
    'OOS',
    'LinearTrend', 
    'ChangePoints',
    'Seasonality',
    'NewTrend',
    'Sales',
    'Constant',
    'Multiplier',
    'Promo',
    'Noise'
]
