from abc import ABC, abstractmethod
from ..models import *

class BaseDB(ABC):
    "Base interface to different type of data storage"
    
    # CRUD operations for properties
    @abstractmethod
    def list_properties(self) -> List[Property]:
        "Return list of properties name and id"
        pass

    @abstractmethod
    def get_property(self, id: str) -> Property:
        "Return property by id"
        pass

    @abstractmethod
    def add_property(self, property: Property) -> str:
        "Add property, return the ID"
        pass

    @abstractmethod
    def update_property(self, id: str, property: Property):
        "Update property by id"
        pass

    @abstractmethod
    def delete_property(self, id: str):
        "Delete property by id"
        pass

    # CRUD operations for areas
    @abstractmethod
    def list_areas(self, property_id: str) -> List[Area]:
        "Return list of areas for a property"
        pass

    @abstractmethod
    def get_area(self, property_id: str, id: str) -> Area:
        "Return area by id"
        pass

    @abstractmethod
    def add_area(self, property_id: str, area: Area) -> str:
        "Add area, return the ID"
        pass

    @abstractmethod
    def update_area(self, property_id: str, id: str, area: Area):
        "Update area by id"
        pass

    # CRUD operations for files
    @abstractmethod
    def add_file(self, property_id: str, filename: str, content: bytes) -> str:
        "Add file, return the ID"
        pass

    @abstractmethod
    def list_files(self, property_id: str) -> List[str]:
        "Return list of files for a property"
        pass

    @abstractmethod
    def get_file_url(self, property_id: str, file_id: str) -> str:
        "Return a URL where the file can be downloaded"
        pass

    @abstractmethod
    def delete_file(self, property_id: str, file_id: str):
        "Delete file by id"
        pass
                    