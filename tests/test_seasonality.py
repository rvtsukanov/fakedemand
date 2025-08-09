import pytest
from fakedemand.series import Row
from fakedemand import factors
import numpy as np


def test_seasonality():
    seasonal_factor = factors.Seasonality()
    seasonal_factor.render()