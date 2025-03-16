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

    def __init__(self, lmax=2, lmin=0.5, rmax=2, rmin=0.5):
        super().__init__()
        self.lmax = lmax
        self.lmin = lmin
        self.rmax = rmax
        self.rmin = rmin

    @property
    def limit_constraints(self):
        return (self.rmin - self.rmax) / self.num_points, (self.rmax - self.lmin) / self.num_points

    def build_own_values(self):
        self.k = np.random.uniform(*self.limit_constraints)
        self.off = np.tan(self.k) * self.num_points
        self.b = np.random.uniform(max(self.rmin - self.k * self.num_points, self.rmin + self.off),
                                    min(self.rmax - self.k * self.num_points, self.rmax - self.off))
        return self.k * np.arange(0, self.num_points) + self.b


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


class Sales(Factor):
    name = 'sales'

    previous_plug_in_dependencies: Optional[List] = []
    previous_plug_in_applier: Optional[Dict] = {OOS: mul, LinearTrend: mul, ChangePoints: mul}

    def __init__(self, level: float,
                 scale: float):
        super().__init__()
        self.level = level
        self.scale = scale

    def build_own_values(self):
        return np.random.normal(self.level, self.scale, self.num_points)


class AddSeasonality(Factor):
    name = 'add_seasonality'

    previous_plug_in_dependencies: Optional[List] = []
    previous_plug_in_applier: Optional[Dict] = None
