import os
from .local import LocalDB
from .firebase import FirebaseDB

if os.environ.get("PRODUCTION") == "true":
    db = FirebaseDB()
else:
    db = FirebaseDB()