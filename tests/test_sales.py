import pytest
from fakedemand.factors import Sales
import datetime
from inspect import signature

@pytest.fixture
def sales():
    s = Sales(level=30, scale=1)
    s.date_left = datetime.date(2023, 1, 1)
    s.date_right = datetime.date(2024, 1, 1)
    return s


def test_sales_own_values(sales):
    # assert sales.date_range
    print(sales.date_range)


def test_types(sales):
    params = list(signature(sales.__init__).parameters.keys())
    print(type(signature(sales.__init__).parameters[params[0]]))
