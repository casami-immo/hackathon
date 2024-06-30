import requests
import io
import pathlib

def load_subtitle(link):
    response = requests.get(link)
    return response.text

TEST_DATA_PATH = pathlib.Path(__file__).parent.joinpath('test_data')

DATA = [
    {'id': 0, 'name': 'Test Property', 'views': [
        {'id': 1, 
         'name': 'Outside', 
         'video': 'https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1906.MOV?alt=media&token=feb01f28-9ca5-4211-b2de-f9003e9c6524',
         'subtitles': TEST_DATA_PATH.joinpath('IMG_1906.srt')},
        {'id': 2,
        'name': 'Building Entry',
        'video': 'https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1907.MOV?alt=media&token=90a9982c-8d66-4795-9a32-8a736aceb6cb',
        'subtitles': TEST_DATA_PATH.joinpath('IMG_1907.srt')
            },
        {'id': 3,
        'name': 'Appartment Entry',
        'video': 'https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1909.MOV?alt=media&token=c93d0dc2-77e8-427e-92fd-04e7aa8303b1'},
        {'id': 4,
        'name': 'Living Room',
        'video': 'https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1910.MOV?alt=media&token=4ffd6c33-41d0-47cd-9307-01be576fb302'},
        {'id': 5,
        'name': 'Kitchen, Bath Room & WC',
        'video': 'https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1911.MOV?alt=media&token=ff2cd027-19fe-4866-9964-b40751f536f2'},
    ]},
]

def get_properties():
    return DATA

def get_property_by_id(id: int):
    for property in DATA:
        if property['id'] == id:
            return property
    return None

def get_views_by_property_id(property_id: int):
    property = get_property_by_id(property_id)
    return property['views']
