import pytest
from fakedemand.series import Row
from fakedemand import factors

import matplotlib
import seaborn as sns
sns.set()
# matplotlib.use('TkAgg')

# TODO: apply factors and rows with different daterange
# TODO: make possible to fix random seed
# TODO: make possible plot two or more factors on a same plot
# TODO: do a feature-view

def test_rows():
    r = Row(idx=0, factors=[factors.LinearTrend(),
                              factors.ChangePoints(),
                              factors.OOS(proba_oos=0.3),
                              factors.Sales(30, 2)])

    r.get_pandas_df()
    r.render_pandas_df('sales')
    # assert not r.df.empty


def test_const():
    r = Row(idx=0, factors=[factors.Constant(10)])
    r.render_pandas_df('constant')

def test_seas():
    r = Row(idx=0, factors=[factors.YearSeasonality(),
                            factors.LinearTrend()])
    r.render_pandas_df('seasonality')

def test_mul():
    # 1. Time-invariant
    # 2. Functionality
    # 3. Parameter-dependent
    # 4. Corner-cases (zeros)
    trend = factors.LinearTrend(descend=True, delta=0.1)
    trend.render()
