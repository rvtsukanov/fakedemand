import datetime
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

class Row:
    date_left = datetime.date(2022, 1, 1)
    date_right = datetime.date(2023, 1, 1)
    date_freq = 'W-MON'

    @property
    def date_range(self):
        return pd.date_range(self.date_left,
                             self.date_right,
                             freq=self.date_freq)

    @property
    def num_points(self):
        return self.date_range.shape[0]

    def __init__(self, idx, factors, **kwargs):
        self.factors = self.activate_factors(factors)
        self.idx = idx  # autoincrease?

    def __repr__(self):
        return f'{self.idx}:row:'

    def activate_factors(self, factors):
        for n, factor in enumerate(factors):
            factor.previous_plug_in_dependencies = factors[:n]  # here it is
            factor.date_left = self.date_left
            factor.date_right = self.date_right
            factor.date_freq = self.date_freq

            factor.apply()

        return factors

    def get_pandas_df(self):
        '''Add melting'''

        d = {}
        for factor in self.factors:
            d[factor.name] = factor.processed_values

        d['date'] = self.date_range
        d['id'] = self.idx

        self.df = pd.DataFrame(d)

    def render_pandas_df(self, column='sales'):
        self.get_pandas_df()
        if column in self.df.columns:
            plt.figure(figsize=(20, 3))
            plt.title(f'{self.__str__()}:{column}')
            sns.lineplot(data=self.df, x='date', y=column, markers='rx')

        plt.show(block=True)
        plt.interactive(False)


