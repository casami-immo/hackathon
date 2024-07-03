import base64
import os
from io import BytesIO

import google.generativeai as genai
from google.ai import generativelanguage as glm
from pdf2image import convert_from_path

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

SYS_PROMPT = """
Role: Real Estate Documentation Analysis Assistant

Task: Analyze real estate documentation and extract specific information.

Instructions:
1. Be precise and only respond with information available in the documents.
2. If requested information is missing, respond with `null`.
3. Omit empty arrays.
4. Provide your response in YAML format without additional explanations.

Output Structure using this JSON schema::
{
  "type": # apartment/house/null, 
  "address": # full address including postal code and city, 
  "floor": # floor number (string),
  "taxe_fonciere": # annual property tax in € (number),
  "condo_fees": # annual condo fees in € (number),
    "diagnostics": # diagnostics information
    {
        "carrez": {
            "total": # Carrez law area (number),
            "date": # Carrez law certification date in YYYY-mm-dd format,
            "rooms": [
                {
                    "name": # room name,
                    "surface": # room surface in m² (number)
                }
            ]
        },
        "dpe": {
            "energy_category": # energy consumption class (A/B/C/D/E/F/G),
            "energy_consumption": # energy consumption in kWh/m²/year (number),
            "emission": # CO2 emissions in kgCO2/m²/year (number),
            "emission_category": # CO2 emissions class (A/B/C/D/E/F/G),
            "date": # diagnosis date in YYYY-mm-dd format,
            "expiring_date": # expiration date in YYYY-mm-dd format,
            "details": {
                "heating": # heating system type,
                "hot_water": # hot water system type,
                "air_conditioning": # air conditioning system type,
                "ventilation": # ventilation system type,
                "windows": # window type
            }
        },
        "asbestos": {
            "date": # asbestos detection date in YYYY-mm-dd format,
            "presence": # true/false if asbestos is present (bool)
        },
        "electricity": {
            "date": # electricity detection date in YYYY-mm-dd format,
            "conform": # true/false if electricity is conform (bool)
        }
    }
}
"""


def convert_pdf_to_grayscale_images(pdf_path, fmt="PNG"):
    images = convert_from_path(pdf_path)

    base64_images = []
    for image in images:
        grayscale_image = image.convert("L")

        buffered = BytesIO()
        grayscale_image.save(buffered, format=fmt)

        base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        base64_images.append(base64_str)

    return base64_images


def extract_gemini(document_path):
    images = convert_pdf_to_grayscale_images(document_path)
    messages = [
        {
            "role": "user",
            "parts": [glm.Blob(mime_type="image/png", data=image) for image in images],
        }
    ]
    model = genai.GenerativeModel(
        "gemini-1.5-flash-latest",
        system_instruction=[SYS_PROMPT],
        generation_config={"response_mime_type": "application/json"},
    )
    response = model.generate_content(messages)
    return response.text
