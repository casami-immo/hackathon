import os
from .local import LocalDB


if os.environ.get("PRODUCTION") == "true":
    db = LocalDB()
else:
    db = LocalDB()