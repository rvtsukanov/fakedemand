import pandas as pd
import numpy as np
import datetime

from typing import Optional, List, Dict

class Factor:
    previous_plug_in_dependencies: Optional[
        List] = []  # это аттрибут-конструктор: тут можно управлять, какие факторы должжны влиять на текущий фактор в конкретном случае
    previous_plug_in_applier: Optional[
        Dict] = {}  # это набор правил, описывающий ВСЕ возможные способы применить все существующие факторы

    date_left = None
    date_right = None
    date_freq = 'W-MON'  # similar to pd.DateIndex freq

    processed_values = None  ## check if apply was applied

    def __init__(self, use_as_feature=False):
        self.use_as_feature = use_as_feature

    @property
    def date_range(self):
        return pd.date_range(self.date_left,
                             self.date_right,
                             freq=self.date_freq)

    @property
    def num_points(self):
        return self.date_range.shape[0]

    def validate_dependencies(self):
        '''Простые проверки, что объекты списка есть в словаре, что нет повторов и тп'''
        if len(set(self.previous_plug_in_dependencies)) != len(self.previous_plug_in_dependencies):
            raise ValueError('Дубли в зависимых факторах')

    #         set_diff = set(list(map(type, self.previous_plug_in_dependencies))) - set(self.previous_plug_in_applier.keys())
    #         if len(set_diff) != 0:
    #             raise ValueError(f'Есть факторы, для которых нет правила применения: {set_diff}')

    def build_own_values(self):
        '''Построить "свои" значения для фичи.'''
        raise NotImplementedError

    def feature_view(self):
        '''Как отобразить фичу, если "механика" не должна совпадать с отображением (мб добавление шума)'''
        raise NotImplementedError

    def apply(self):
        '''Микс собственных значений и значений из build+transform'''
        self.validate_dependencies()
        own_values = self.build_own_values()

        # reduce? #wrong order?
        for transform in self.previous_plug_in_dependencies:
            if type(transform) in self.previous_plug_in_applier:
                own_values = self.previous_plug_in_applier[type(transform)](transform.processed_values,
                                                                            own_values)  # idk, mb do it better; invent reducer?
        self.processed_values = own_values
        return own_values


class Sampler:
    def __init__(self):
        # float
        # int
        pass

