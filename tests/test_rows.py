import pytest
from fakedemand.series import Row
from fakedemand.factors.linear_trend import LinearTrend
from fakedemand.factors.change_points import ChangePoints
from fakedemand.factors.oos import OOS
from fakedemand.factors.sales import Sales
from fakedemand.factors.constant import Constant
from fakedemand.factors.seasonality import Seasonality

import matplotlib
import seaborn as sns
sns.set()
# matplotlib.use('TkAgg')

# TODO: apply factors and rows with different daterange
# TODO: make possible to fix random seed
# TODO: make possible plot two or more factors on a same plot
# TODO: do a feature-view

def test_rows():
    r = Row(idx=0, factors=[LinearTrend(),
                              ChangePoints(),
                              OOS(proba_oos=0.3),
                              Sales(30, 2)])

    r.get_pandas_df()
    r.render_pandas_df('sales')
    # assert not r.df.empty


def test_const():
    r = Row(idx=0, factors=[Constant(10)])
    r.render_pandas_df('constant')

def test_seas():
    r = Row(idx=0, factors=[Seasonality(),
                            LinearTrend()])
    r.render_pandas_df('seasonality')

def test_mul():
    # 1. Time-invariant
    # 2. Functionality
    # 3. Parameter-dependent
    # 4. Corner-cases (zeros)
    trend = LinearTrend(descend=True, delta=0.1)
    trend.render()
