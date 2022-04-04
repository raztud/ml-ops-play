from typing import Union

from pydantic import BaseModel


class Prediction(BaseModel):
    prediction: Union[float, int]


class RequestModel(BaseModel):
    gdp: int
