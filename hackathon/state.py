from typing import List

import os
import reflex as rx
from backend.database import in_memory as db
from backend.assistant import answer


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}

class State(rx.State):
    """The app state."""

    # # Current property id
    current_property_id: int = 0

    # Current area index
    current_area_idx: int = 0

    question: str

    chat_history: List[QA] = []

    processing : bool = False

    @rx.var
    def current_property(self) -> dict:
        """Get the current property."""
        return self.current_property_id
    
    @rx.var
    def current_area(self) -> str:
        """Get the current area name."""
        areas = db.get_areas_by_property_id(self.current_property_id)
        return areas[self.current_area_idx]
    
    @rx.var
    def video_url(self) -> str:
        """Get the current video URL."""
        return self.current_area["video"]
    
    @rx.var
    def areas_names(self) -> list[str]:
        """Get the list of areas."""
        areas = db.get_areas_by_property_id(self.current_property_id)
        return [area["name"] for area in areas]
    
    @rx.var
    def current_area_name(self) -> str:
        """Get the current area name."""
        return self.areas_names[self.current_area_idx]
    
    def next_area(self):
        """Switch to the next area."""
        if self.current_area_idx == len(self.areas_names) - 1:
            self.current_area_idx = 0
        else:
            self.current_area_idx += 1

    def previous_area(self):
        """Switch to the previous area."""
        if self.current_area_idx == 0:
            self.current_area_idx = len(self.areas_names) - 1
        else:
            self.current_area_idx -= 1

    def switch_area(self, area_name: str):
        """Switch to a specific area."""
        self.current_area_idx = self.areas_names.index(area_name)

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Get the answer from the API
        self.chat_history.append(QA(question=question, answer=""))
        async for answer_text in answer(
            question, self.chat_history, context={"property_id": self.current_property, "current_area": self.current_area_name}):
            if answer_text is not None:
                self.chat_history[-1].answer += answer_text
            else:
                # Handle the case where answer_text is None, perhaps log it or assign a default value
                # For example, assigning an empty string if answer_text is None
                answer_text = ""
                self.chat_history[-1].answer += answer_text
            yield
        # Toggle the processing flag.
        self.processing = False
        yield