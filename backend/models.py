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
    name: str = ""
    surface: float = None


class Carrez(rx.Base):
    rooms: List[CarrezArea] = []
    date: str = None
    total: float = None


class DPEDetails(rx.Base):
    heating_type: str = None
    hot_water_type: str = None
    air_conditioning: bool = None
    ventilation_type: str = None
    windows_type: str = None


class DPE(rx.Base):
    energy_category: str = None
    energy_consumption: float = None
    gaz_emission_category: str = None
    gaz_emission: float = None
    date: str = None
    expiring_date: str = None
    details: DPEDetails = None


class Abestos(rx.Base):
    presence: bool = None
    date: str = None


class Electricity(rx.Base):
    conform: bool = None
    date: str = None


class Diagnostics(rx.Base):
    carrez: Carrez = None
    dpe: DPE = None
    abestos: Abestos = None
    electricity: Electricity = None


class Property(rx.Base):
    id: str = str(uuid4())
    name: str = ""
    address: str = ""
    floor: int = 0
    taxe_fonciere: float = None
    condo_fees: float = None
    diagnostics: Diagnostics = None
    areas: Dict[str, Area] = {}
