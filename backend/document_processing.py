from .database.local import LocalDB

MOCK_DATA = LocalDB().get_property("0")


def extract_data(files):
    # dummy function, replace later
    return MOCK_DATA.dict()