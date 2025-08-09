import pytest
from fakedemand.series import Row
from fakedemand import factors
import numpy as np

def test_linear_trend_asc():
    '''
    Проверка корректности роста тренда
    '''
    trend_factor_asc = factors.LinearTrend(descend=False, delta=0.1)
    trend_factor_desc = factors.LinearTrend(descend=True, delta=0.1)

    assert trend_factor_asc.own_values[-1] > trend_factor_asc.own_values[0]
    assert trend_factor_desc.own_values[0] > trend_factor_desc.own_values[-1]


def test_linear_trend_big_delta():
    with pytest.raises(Exception) as exc:
        factors.LinearTrend(descend=False, delta=3)
        assert exc


def test_linear_trend_delta_amount():
    for delta in np.random.rand(2):
        # print(delta)
        trend_factor_asc = factors.LinearTrend(descend=False, delta=delta)
        trend_factor_desc = factors.LinearTrend(descend=True, delta=delta)

        assert np.allclose(trend_factor_asc.own_values.max() - trend_factor_asc.own_values.min(), 2 * delta, rtol=1e-1)
        assert np.allclose(trend_factor_desc.own_values.max() - trend_factor_desc.own_values.min(), 2 * delta, rtol=1e-1)


def test_linear_trend_ones_centered():
    trend_factor_asc = factors.LinearTrend(descend=False, delta=0.1)

    # trend_factor_asc.own_values = trend_factor_asc.own_values[:-2]
    n = trend_factor_asc.own_values.shape[0]

    print(trend_factor_asc.own_values[n // 2], n)
    assert np.allclose(trend_factor_asc.own_values[n // 2], 1, rtol=1e-1)


