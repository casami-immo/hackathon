import reflex as rx
from backend.database import in_memory as db
from backend.assistant import answer
from typing import List


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


class Property(rx.Base):
    """A property object."""

    name: str
    id: str


DEFAULT_CHATS = {
    "Intros": [],
}


class VisitState(rx.State):
    """The app state."""

    # Current area index
    current_area_idx: int = 0

    question: str

    chat_history: List[QA] = []

    processing: bool = False

    @property
    def current_property_id(self) -> str:
        """Get the current property."""
        try:
            return str(self.router.page.params["property_id"])
        except KeyError:
            None
    
    @property
    def current_area(self) -> str:
        """Get the current area name."""
        try:
            areas = db.get_areas_by_property_id(self.current_property_id)
            return areas[self.current_area_idx]
        except:
            return None

    @rx.var
    def video_url(self) -> str:
        """Get the current video URL."""
        try:
            return self.current_area["video"]
        except:
            return ""

    @rx.var
    def areas_names(self) -> list[str]:
        """Get the list of areas."""
        try:
            areas = db.get_areas_by_property_id(self.current_property_id)
            return [area["name"] for area in areas]
        except:
            return []

    @rx.var
    def current_area_name(self) -> str:
        """Get the current area name."""
        try:
            return self.areas_names[self.current_area_idx]
        except:
            return ""

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
            question,
            self.chat_history,
            context={
                "property_id": self.current_property_id,
                "current_area": self.current_area_name,
            },
        ):
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
