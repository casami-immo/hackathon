import requests
import io
import pathlib
from uuid import uuid4


def load_subtitle(link):
    response = requests.get(link)
    return response.text


TEST_DATA_PATH = pathlib.Path(__file__).parent.joinpath("test_data")

DATA = [
    {
        "id": "0",
        "name": "Test Property",
        "address": "20 rue Raspail, 92300 Levallois-Perret",
        "floor": "5",
        "taxe_fonciere": "951",
        "condo_fees(annual)": "536",
        "diagnostics": {
            "carrez": {
                    "total": "34.67",
                    "date": "2008-05-21",
                    "rooms": [
                        {
                            "name": "Hall",
                            "surface": "3.22"
                        },
                        {
                            "name": "Kitchen",
                            "surface": "3.83"
                        },
                        {
                            "name": "Bathroom & WC",
                            "surface": "3.22"
                        },
                        {
                            "name": "Living Room",
                            "surface": "23.64"
                        }
                            ]
                      },
            "dpe": {
                    "energy_category": "D",
                    "energy_consumption(kWh/m2/yr)": "212",
                    "emission(kgCO2/m2/yr)": "6",
                    "emission_category": "B",
                    "date": "2022-03-21",
                    "expiring_date": "2023-03-21",
                    "details": {
                        "heating": "electric",
                        "hot_water": "electric",
                        "air_conditioning": "no",
                        "ventilation": "natural",
                        "windows": "double glazing",
                    },
                  },
            "asbestos": {
                    "date": "2000-06-07",
                    "presence": "no",
                  },
            "electricity": {
                    "date": "2000-06-07",
                    "conform": "no",
                  },
        },
        "areas": [
            {
                "id": 1,
                "name": "Outside",
                "video": "https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1906.MOV?alt=media&token=feb01f28-9ca5-4211-b2de-f9003e9c6524",
                "subtitles": TEST_DATA_PATH.joinpath("IMG_1906.srt"),
                "qa":[
                    {
                        "question": "Year of construction?",
                        "answer": "90s"
                    },
                    {
                        "question": "How many floors does the building have?",
                        "answer": "The building has 6 floors"
                    },
                    {
                        "question": "Is it close to public transport?",
                        "answer": "The L trains is 5 minutes away and the metro 3 is 12 minutes away. You can reach LaDefense or Saint Lazare in 20minutes"
                    },
                    {
                        "question": "Is there a parking space?",
                        "answer": "Yes, there is a parking space"
                    },
                    {
                        "question": "Where is the address?",
                        "answer": "The adress is 20 rue Raspail"
                    },
                    {
                        "question": "What are the commidity around?",
                        "answer": """The place Jean Zay is 2 minutes away with many restaurants and a fresh product market. You also have the community swimming pool next to the building.
                        The city hall and post office are 10 minutes away, and a bit further there is the SoOuest shopping center and the cinema. 
                        """
                    },
                ]
            },
            {
                "id": 2,
                "name": "Building Entry",
                "video": "https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1907.MOV?alt=media&token=90a9982c-8d66-4795-9a32-8a736aceb6cb",
                "subtitles": TEST_DATA_PATH.joinpath("IMG_1907.srt"),
                "qa": [
                    {
                        "question": "How is the building secured?",
                        "answer": "There is a digicode and interphone"
                    },
                    {
                        "time": "00:00:13.000",
                        "question": "What is this door?",
                        "answer": "This is the recycling room, you can put your recycling here"
                    },
                    {
                        "question": "Is there a concierge?",
                        "answer": "No"
                    },
                    {
                        "question": "Are there 2 elevators?",
                        "answer": "Yes, the building is actually a twin building with 2 parts. Each part has its own elevator"
                    },
                    {
                        "question": "Is the garden accessible?",
                        "answer": "No, the garden is not accessible by the residents."
                    },
                    {
                        "time": "00:00:41.000",
                        "question": "What is this area?",
                        "answer": "This is a part of the building for commercial used. It is owned by a company. They just bought the place and renovating it to make an office space."
                    },
                    {
                        "time": "00:00:38.000",
                        "question": "What are those doors?",
                        "answer": "The 2 doors next to the elevators are the stairscase. One go to the cellar and parking and the other go up to the appartments."
                    },
                ]
            },
            {
                "id": 3,
                "name": "Appartment Entry",
                "video": "https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1909.MOV?alt=media&token=c93d0dc2-77e8-427e-92fd-04e7aa8303b1",
                "qa": [
                    {
                        "question": "Whivh floor is the appartment?",
                        "answer": "It is at the 5th floors"
                    },
                    {
                        "question": "How many appartments are on this floor?",
                        "answer": "There are 4 appartments on this floor"
                    },
                ]
            },
            {
                "id": 4,
                "name": "Living Room",
                "video": "https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1910.MOV?alt=media&token=4ffd6c33-41d0-47cd-9307-01be576fb302",
                "qa": [
                    {
                        "question": "What is the surface of the living room?",
                        "answer": "The surface is 23.64m2"
                    },
                    {
                        "question": "Is the floor real wood?",
                        "answer": "Yes it is real parquet"
                    },
                    {
                        "question": "Is this connected to optical fiber?",
                        "answer": "Yes, the connection is close to the windows"
                    },
                    {
                        "question": "What is the orientation of the living room?",
                        "answer": "The living room's window is facing west"
                    },
                    {
                        "question": "Was the walls repainted recently?",
                        "answer": "The wall was repainted last year in 2023."
                    },
                    {
                        "time": "00:00:49.000",
                        "question": "What is this big courtyard?",
                        "answer": "This is an elementary school. It is very quiet during the weekend and holidays."
                },
                    { 
                        "question": "Is the windows double glazing?",
                        "answer": "Yes, the windows are double glazing"
                    },
                    {
                        "question": "Is the windows blind manual or automatic?",
                        "answer": "The blinds are automatic"
                    },
                    {
                        "question": "What is the heating type?",
                        "answer": "The heating is electric"
                    }
                ]
            },
            {
                "id": 5,
                "name": "Kitchen, Bath Room & WC",
                "video": "https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1911.MOV?alt=media&token=ff2cd027-19fe-4866-9964-b40751f536f2",
                "qa": [
                    {
                        "question": "What is the surface of the kitchen?",
                        "answer": "The surface is 3.83m2"
                    },
                    {
                        "question": "What is the surface of the bathroom & WC?",
                        "answer": "The surface is 3.22m2"
                    },
                    {
                        "question": "Is the kitchen equipped?",
                        "answer": """Yes, the kitchen is equipped with a fridge, a stove, a microwave, induction hob,
                        a sink and a washing machine."""
                    },
                    {
                        "question": "Was the kitchen renovated recently?",
                        "answer": "The kitchen was renovated in 2023"
                    },
                    {
                        "question" : "Is the kitchen floor real wood?",
                        "answer": "No, the floor is PVC with wood pattern, it is easy to clean and maintain",
                    },
                    {
                        "question": "Is the bathroom equipped?",
                        "answer": "Yes, the bathroom is equipped with a bath, a sink and a WC"
                    },
                    {
                        "question": "What is the bathroom floor type?",
                        "answer": "The floor is tiled"
                    },
                    {
                        "time": "00:01:19.000",
                        "question": "What is this?",
                        "answer": "This is the hot water tank, the hot water is electric"
                    },
                ]
            },
        ],
    },
]


def list_properties():
    data = [
        {
            "name": property["name"],
            "id": property["id"]
        }
        for property in DATA
    ]
    return data

def new_property(property_data: dict):
    property_data["id"] = str(uuid4())
    property_data["areas"] = []
    property_data["name"] = property_data["address"]
    DATA.append(property_data)
    return property_data["id"]

def delete_property(property_id: int):
    for i, property in enumerate(DATA):
        if property["id"] == property_id:
            return DATA.pop(i)
    return None

def update_property(property_id: int, property_data: dict):
    for i, property in enumerate(DATA):
        if property["id"] == property_id:
            DATA[i] = property_data
            return property_data
    return None

def new_area(property_id: str, area_data: dict):
    property = get_property_by_id(property_id)
    area_data["id"] = len(property["areas"])
    property["areas"].append(area_data)
    return area_data

def update_area(property_id: str, area_id: int, area_data: dict):
    property = get_property_by_id(property_id)
    for i, area in enumerate(property["areas"]):
        if area["id"] == area_id:
            property["areas"][i] = area_data
            return area_data
    return None

def delete_area(property_id: str, area_id: int):
    property = get_property_by_id(property_id)
    for i, area in enumerate(property["areas"]):
        if area["id"] == area_id:
            return property["areas"].pop(i)
    return None


def get_property_by_id(id: str):
    for property in DATA:
        if property["id"] == id:
            return property
    return None


def get_areas_by_property_id(property_id: str):
    property = get_property_by_id(property_id)
    return property["areas"]