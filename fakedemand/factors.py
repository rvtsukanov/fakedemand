from fakedemand.core import Factor
from typing import List, Optional, Dict

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from functools import reduce
from operator import mul, add

import datetime
from fakedemand._types import Probability, Precision, Number, Coefficient

class OOS(Factor):
    name = 'oos'
    base = 10

    previous_plug_in_dependencies: Optional[List] = []
    previous_plug_in_applier: Optional[Dict] = {}

    def __init__(self, proba_oos: Probability,
                 precision: Precision = 2):
        super().__init__()
        self.proba_oos = 1 - proba_oos
        self.precision = precision

    def build_own_values(self):
        mask = np.random.binomial(self.base ** self.precision, self.proba_oos,
                                  self.num_points) / self.base ** self.precision
        return np.where(mask > self.proba_oos, 1, mask)


class LinearTrend(Factor):
    name = 'trend'

    def __init__(self, descend=True, delta=0.5):
        self.descend = descend
        self.delta = delta

        if self.delta > 1 or self.delta < 0:
            raise ValueError('delta parameter should be (0, 1)')

        super().__init__()

    @property
    def limit_constraints(self):
        return (self.rmin - self.rmax) / self.num_points, (self.rmax - self.lmin) / self.num_points

    def build_own_values(self):
        sign = -1 if self.descend else 1
        k = sign * 2 * self.delta / self.num_points
        b = 1 + -1 * sign * self.delta
        return k * np.arange(0, self.num_points) + b


class ChangePoints(Factor):
    name = 'changepoints'

    def __init__(self,
                 num_change_points: Number = 3,
                 min_level: Coefficient = 0.5,
                 max_level: Coefficient = 2):
        super().__init__()
        self.num_change_points = num_change_points
        self.min_level = min_level
        self.max_level = max_level

    def time_intervals(self):
        quotient = int(np.floor(self.num_points / self.num_change_points))
        return np.random.permutation(
            [quotient] * (self.num_change_points - 1) + [self.num_points - quotient * (self.num_change_points - 1)])

    def build_own_values(self):
        return np.array(
            reduce(add, [[np.random.uniform(self.min_level, self.max_level)] * i for i in self.time_intervals()]))


class Seasonality(Factor):
    name = 'seasonality'

    def __init__(self, type='year', peak='july'):
        self.type = type
        self.peak = peak
        super().__init__()

    def get_offset(self):
        # w=27
        # self.date_range[self.date_range.month == 7][0]
        first_day_of_peak_period = self.date_range[self.date_range.month == 7][0]
        first_day_of_period = self.date_range[0]
        return first_day_of_peak_period - first_day_of_period

    def build_own_values(self):
        k = 1
        alpha = 0.2
        phi = int((self.get_offset().days) / 7)
        # phi = 5
        return alpha * np.sin(k * np.linspace(0, 2 * np.pi, num=self.num_points) + phi / self.num_points * 2 * np.pi) + 1


class NewTrend(Factor):
    def __init__(self, delta=0.2):
        self.delta = delta


    def build_own_values(self):
        return np.linspace(0, self.num_points)


class Sales(Factor):
    name = 'sales'

    previous_plug_in_dependencies: Optional[List] = []
    previous_plug_in_applier: Optional[Dict] = {OOS: mul, LinearTrend: mul, ChangePoints: mul,
                                                Seasonality: mul}

    def __init__(self, level: float,
                 scale: float):
        super().__init__()
        self.level = level
        self.scale = scale

    def build_own_values(self):
        return np.random.normal(self.level, self.scale, self.num_points)



class Constant(Factor):
    name = 'constant'
    def __init__(self, value):
        self.value = value

    def build_own_values(self):
        return np.array([self.value] * self.num_points)


class Multiplier(Constant):

    def __init__(self, value):
        self.value = value
