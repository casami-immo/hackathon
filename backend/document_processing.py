from backend.doc_processing.gemeni import extract_gemini


def extract_data(file_path):
    response = extract_gemini(file_path)
    return response