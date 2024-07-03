import json

from backend.doc_processing.gemeni import extract_gemini
from backend.models import Property


def extract_data(file_paths):
    response = extract_gemini(file_paths)
    property = Property(**json.loads(response))
    property.name = f"{property.type} - {property.diagnostics.carrez.total}m²"
    return property