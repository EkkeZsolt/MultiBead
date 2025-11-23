from pydantic import BaseModel
from typing import List


class MeasurementPointDTO(BaseModel):
    x: float
    y: float


class MeasurementCreateDTO(BaseModel):
    points: List[MeasurementPointDTO]


class UserCreateDTO(BaseModel):
    name: str


class UserDTO(BaseModel):
    id: int
    name: str
