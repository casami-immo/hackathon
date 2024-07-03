import datetime
from typing import Dict, List
from uuid import uuid4

import reflex as rx
from pydantic.v1 import root_validator


class File(rx.Base):
    id: str = str(uuid4())
    filename: str
    url: str


class QA(rx.Base):
    question: str
    answer: str


class Area(rx.Base):
    id: str = str(uuid4())
    name: str = ""
    description: str = ""
    video: File = None
    qa: List[QA] = []


class CarrezArea(rx.Base):
    name: str
    surface: float


class Carrez(rx.Base):
    rooms: List[CarrezArea]
    date: datetime.date
    total: float

    @root_validator(pre=True)
    def parse_date(cls, values):
        value = values.get("date")
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
        values["date"] = value
        return values


class DPEDetails(rx.Base):
    heating_type: str
    hot_water_type: str
    air_conditioning: bool
    ventilation_type: str
    windows_type: str


class DPE(rx.Base):
    energy_category: str
    energy_consumption: float
    gaz_emission_category: str
    gaz_emission: float
    date: datetime.date
    expiring_date: datetime.date
    details: DPEDetails

    @root_validator(pre=True)
    def parse_date(cls, values):
        value = values.get("date")
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
        values["date"] = value
        return values


class Abestos(rx.Base):
    presence: bool
    date: datetime.date

    @root_validator(pre=True)
    def parse_date(cls, values):
        value = values.get("date")
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
        values["date"] = value
        return values


class Electricity(rx.Base):
    conform: bool
    date: datetime.date

    @root_validator(pre=True)
    def parse_date(cls, values):
        value = values.get("date")
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
        values["date"] = value
        return values


class Diagnostics(rx.Base):
    carrez: Carrez
    dpe: DPE
    abestos: Abestos
    electricity: Electricity


class Property(rx.Base):
    id: str = str(uuid4())
    name: str = ""
    address: str = ""
    floor: int = 0
    taxe_fonciere: float = None
    condo_fees: float = None
    diagnostics: Diagnostics = None
    areas: Dict[str, Area] = {}
