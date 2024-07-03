"Firebase Firestore backend and Firebase Storage for files"
import os
from uuid import uuid4
import base64

import firebase_admin.firestore
import firebase_admin.storage

from backend.models import Property, Area, File
from .base import BaseDB
import firebase_admin
from firebase_admin import credentials





class FirebaseDB(BaseDB):
    "Firebase Firestore backend"

    def __init__(self):
        with open('/tmp/serviceAccountKey.json', 'w') as f:
            json_string = base64.b64decode(os.environ['FIREBASE_CREDENTIALS']).decode('utf-8')
            f.write(json_string)
        cred = credentials.Certificate('/tmp/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        self.db = firebase_admin.firestore.client()
        self.storage = firebase_admin.storage.bucket("hackathon-lablab")

    def get_property(self, id: str) -> Property:
        "Get a property by ID"
        property_ref = self.db.collection('properties').document(id)
        property_data = property_ref.get().to_dict()
        if property_data is None:
            return None
        return Property(**property_data)
    
    def list_properties(self) -> list[Property]:
        "Get all properties"
        properties = self.db.collection('properties').stream()
        return [Property(**p.to_dict()) for p in properties]
    
    def add_property(self, property: Property) -> Property:
        "Add a property"
        property_ref = self.db.collection('properties').document()
        property.id = property_ref.id
        property_ref.set(property.dict())
        return property.id
    
    def update_property(self, id: str, property: Property):
        "Update a property"
        property.id = id
        property_ref = self.db.collection('properties').document(id)
        property_ref.set(property.dict())

    def delete_property(self, id: str):
        "Delete a property"
        property_ref = self.db.collection('properties').document(id)
        property_ref.delete()

    def list_areas(self, property_id: str) -> list[Area]:
        "Get all areas for a property"
        areas = self.db.collection('properties').document(property_id).collection('areas').stream()
        return [Area(**a.to_dict()) for a in areas]
    
    def get_area(self, property_id: str, id: str) -> Area:
        "Get an area by ID"
        area_ref = self.db.collection('properties').document(property_id).collection('areas').document(id)
        area_data = area_ref.get().to_dict()
        if area_data is None:
            return None
        return Area(**area_data)
    
    def add_area(self, property_id: str, area: Area) -> Area:
        "Add an area"
        area_ref = self.db.collection('properties').document(property_id).collection('areas').document()
        area.id = area_ref.id
        area_ref.set(area.dict())
        return area.id
    
    def update_area(self, property_id: str, id: str, area: Area):
        "Update an area"
        area.id = id
        area_ref = self.db.collection('properties').document(property_id).collection('areas').document(id)
        area_ref.set(area.dict())

    def delete_area(self, property_id: str, id: str):
        "Delete an area"
        area_ref = self.db.collection('properties').document(property_id).collection('areas').document(id)
        area_ref.delete()

    def add_file(self, filename: str, content: bytes) -> str:
        "Add a file"
        file_id = str(uuid4())
        file_ref = self.storage.blob(f"{file_id}/{filename}")
        file_ref.upload_from_string(content, content_type='application/octet-stream')
        file_ref.make_public()
        
        file_obj = File(
            id=file_id, 
            filename=filename, 
            url=file_ref.public_url)
        
        self.db.collection('files').document(file_id).set(file_obj.dict())
        return file_id
    
    def get_file(self, id: str) -> File:
        "Get a file by ID"
        file_ref = self.db.collection('files').document(id)
        file_data = file_ref.get().to_dict()
        if file_data is None:
            return None
        return File(**file_data)
    
    def delete_file(self, id: str):
        "Delete a file"
        file_ref = self.db.collection('files').document(id)
        file_dict = file_ref.get().to_dict()
        file_ref.delete()
        blob = self.storage.blob(f"{id}/{file_dict['filename']}")
        blob.delete()

    def list_files(self) -> list[File]:
        "Get all files"
        files = self.db.collection('files').stream()
        return [File(**f.to_dict()) for f in files]
