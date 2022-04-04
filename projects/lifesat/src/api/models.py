from typing import Union

from pydantic import BaseModel


class LivesatPrediction(BaseModel):
    prediction: Union[float, int]


class LivesatRequestModel(BaseModel):
    gdp: int
