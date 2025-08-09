#!/usr/bin/env python3
"""
Example usage of fakedemand package.
This file demonstrates how to use the Sales factor with Row.

To run this example:
    python -m fakedemand.fakedemand
"""

from fakedemand.series import Row
from fakedemand.factors.sales import Sales
from fakedemand.factors.seasonality import Seasonality

def main():
    """Main function to demonstrate fakedemand usage."""
    print("Creating a Row with Sales factor...")
    s = Seasonality(peaks=['saturday', 'may'], amplitude=0.3)
    s.date_freq = 'W'

    r1 = Row(idx=1, factors=[s])
    
    print("Rendering the pandas dataframe...001")
    print(s.render())


if __name__ == "__main__":
    pass
    # main()


