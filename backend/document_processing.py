import json

from backend.doc_processing.gemeni import extract_gemini
from backend.models import Property


def extract_data(file_paths):
    response = extract_gemini(file_paths)
    return Property(**json.loads(response))
