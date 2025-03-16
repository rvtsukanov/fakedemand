# Definition of macroparameters for sampling
from typing import Optional, Any

import numpy as np

class ParamType:
    base_type: type = None
    min: Optional[Any] = None
    max: Optional[Any] = None

    @classmethod
    def _sampler(cls):
        if cls.base_type == int:
            return np.random.rand
        elif cls.base_type == float:
            return np.random.randint

    @classmethod
    def sample(cls):
        pass
        # return cls._sampler(low=cls.min, high=cls.max)

class Probability(ParamType):
    base_type = float
    min: float = 0.
    max: float = 1.


class Precision(ParamType):
    base_type = int
    min: int = 0
    max: int = 5


class Number(ParamType):
    base_type = int
    min: int = 0
    max: int = 100


class Coefficient(ParamType):
    min = -100.
    max = 100.


p = Precision()
proba = Probability()
print(p._sampler())
# print(proba._sampler())
print(p.sample())