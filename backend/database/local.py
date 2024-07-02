"Local database implementation for testing purposes"

import os
import json
from uuid import uuid4

import reflex as rx
from typing import Dict

from backend.models import Area, List, Property

from .base import BaseDB


class DataBase(rx.Base):
    properties: Dict[str, Property] = {}


class LocalDB(BaseDB):
    """
    Local database using file system. 
    Data are stored in JSON file in ./test_data/data.json. 
    The files are stored in /uploaded_files folder, 
    This is not persistent because each deployment will have its own file system.
    """

    def __init__(self):
        self.datadir = os.path.realpath(__file__).replace("local.py", "test_data/")
        self.filedir = rx.get_upload_dir()
        if not os.path.exists(f"{self.datadir}/data.json"):
            os.makedirs(self.datadir, exist_ok=True)
            self.data = DataBase()
            self._save_data()

        self.data = self._load_data()  # cache in memory

    def _load_data(self):
        return DataBase.parse_file(f"{self.datadir}/data.json", content_type="json").dict()
        # with open(f"{self.datadir}/data.json", "r") as f:
        #     data = DataBase(**json.load(f))
        #     return data.
        
    def _save_data(self):
        with open(f"{self.datadir}/data.json", "w") as f:
            f.write(DataBase(**self.data).json())

    def add_property(self, property: Property) -> str:
        property.id = str(uuid4())
        self.data["properties"][property.id] = property.dict()
        self._save_data()
        return property.id
    
    def list_properties(self) -> List[Property]:
        return [Property(**v) for v in self.data["properties"].values()]
    
    def get_property(self, id: str) -> Property:
        return Property(**self.data["properties"][id])
    
    def update_property(self, id: str, property: Property):
        data_dict = property.dict()
        data_dict["id"] = id
        self.data["properties"][id] = data_dict
        self._save_data()

    def delete_property(self, id: str):
        self.data["properties"].pop(id)
        self._save_data()

    def add_area(self, property_id: str, area: Area) -> str:
        area.id = str(uuid4())
        self.data["properties"][property_id]["areas"][area.id] = area.dict()
        self._save_data()
        return area.id
    
    def list_areas(self, property_id: str) -> List[Area]:
        return [Area(**v) for v in self.data["properties"][property_id]["areas"].values()]
    
    def get_area(self, property_id: str, id: str) -> Area:
        return Area(**self.data["properties"][property_id]["areas"][id])
    
    def delete_area(self, property_id: str, id: str):
        self.data["properties"][property_id]["areas"].pop(id)
        self._save_data()
        
    def update_area(self, property_id: str, id: str, area: Area):
        data_dict = area.dict()
        data_dict["id"] = id
        self.data["properties"][property_id]["areas"][id] = data_dict
        self._save_data()

    def get_file_url(self, property_id: str, file_id: str) -> str:
        filename = self.data["properties"][property_id]["files"][file_id]
        return f"http://localhost:8000/_upload/{property_id}/{filename}"

    def add_file(self, property_id: str, filename: str, content: bytes) -> str:
        file_id = str(uuid4())
        with open(f"{self.filedir}/{property_id}/{filename}", "wb") as f:
            f.write(content)
        self.data["properties"][property_id]["files"][file_id] = filename
    
    def list_files(self, property_id: str) -> List[str]:
        return [filename for filename in self.data["properties"][property_id]["files"].values()]
    
    def delete_file(self, property_id: str, file_id: str):
        filename = self.data["properties"][property_id]["files"].pop(file_id)
        os.remove(f"{self.filedir}/{property_id}/{filename}")
