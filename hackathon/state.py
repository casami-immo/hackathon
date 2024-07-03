from typing import List

import os
import reflex as rx
from backend.database import db
from backend.assistant import answer


class AppState(rx.State):
    """The app state."""

    # # Current property id
    is_host: bool = False
    