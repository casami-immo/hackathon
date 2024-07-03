from typing import List, Dict
from datetime import datetime
from uuid import uuid4

import reflex as rx


class File(rx.Base):
    id: str = str(uuid4())
    filename: str
    url: str


class QA(rx.Base):
    question: str
    answer: str

class Area(rx.Base):
    id: str = str(uuid4())
    name: str
    description: str
    video: File
    qa : List[QA]

class CarrezArea(rx.Base):
    name: str
    surface: float

class Carrez(rx.Base):
    rooms: List[CarrezArea]
    date: datetime
    total: float


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
    date: datetime
    expiring_date: datetime
    details: DPEDetails


class Abestos(rx.Base):
    presence: bool
    date: datetime


class Electricity(rx.Base):
    conform: bool
    date: datetime


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


