import reflex as rx
from hackathon.components.layout import apply_layout
from backend.database import db
from backend.models import Area, File, QA, List
from backend.generate_questions import suggest_questions
from uuid import uuid4
from pydantic import Field


class Question(rx.Base):
    text: str
    id: str
    answer: str


class QuestionsList(rx.Base):
    data: List[Question] = []


class AreaState(rx.State):
    """The app state."""

    video_file_id: str = ""
    video_url: str = ""
    questions: QuestionsList = QuestionsList()
    generating: bool = False
    name: str = ""
    description: str = ""
    uploading: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        self.uploading = True
        yield
        for file in files:
            upload_data = await file.read()

            self.video_file_id = db.add_file(
                filename=file.filename,
                content=upload_data,
            )
            self.video_url = db.get_file(self.video_file_id).url
            self.video_url.replace(
                "http://localhost:8000/", f"http://{self.router.headers.host}/"
            )
        self.uploading = False

    async def create_area(self):
        """Create a new area."""
        area_id = db.add_area(
            property_id=self.router.page.params["property_id"],
            area=Area(
                name=self.name,
                description=self.description,
                video=db.get_file(self.video_file_id),
                qa=[
                    QA(
                        question=question.text,
                        answer=question.answer,
                    )
                    for question in self.questions.data
                ],
            ),
        )
        self.video_file_id = ""
        self.video_url = ""
        self.questions.data = []
        self.name = ""
        self.description = ""

        return rx.redirect(
            f"/properties/{self.router.page.params['property_id']}/areas/{area_id}/caption"
        )

    def update_name(self, name: str):
        self.name = name

    def update_desc(self, description: str):
        self.description = description

    def update_question(self, question_id: str, text: str):
        for question in self.questions.data:
            if question.id == question_id:
                question.text = text

    def update_answer(self, question_id: str, answer: str):
        for question in self.questions.data:
            if question.id == question_id:
                question.answer = answer

    def add_question(self, question: str, answer: str):
        self.questions.data.append(
            Question(
                text=question,
                answer=answer,
                id=str(uuid4()),
            )
        )

    def delete_question(self, question_id: str):
        print(question_id, self.questions.data)
        self.questions.data = [q for q in self.questions.data if q.id != question_id]

    async def suggest_faq(self):
        self.generating = True
        yield
        new_questions = suggest_questions(
            name=self.name,
            description=self.description,
            video_url=self.video_url,
            current_questions=[q.text for q in self.questions.data],
        )

        for question in new_questions:
            self.add_question(question, "")
            yield
        self.generating = False


def upload_zone():
    return rx.upload(
        rx.cond(
            AreaState.uploading,
            rx.chakra.spinner("Uploading video..."),
            rx.vstack(
                rx.button("Select File", bg="white"),
                rx.text("Drag and drop files here or click to select files"),
            ),
        ),
        id="upload2",
        multiple=True,
        accept={
            "video/mp4": [".mp4"],
            "video/mov": [".mov"],
        },
        max_files=1,
        disabled=False,
        on_drop=AreaState.handle_upload(rx.upload_files(upload_id="upload2")),
        padding="5em",
    )


def qa_item(question: Question):
    return rx.chakra.card(
        rx.chakra.hstack(
            rx.chakra.vstack(
                rx.chakra.hstack(
                    rx.chakra.text("Q:", padding_x="8px", as_="b"),
                    rx.chakra.input(
                        value=question.text,
                        on_change=lambda text: AreaState.update_question(
                            question.id, text
                        ),
                        is_disabled=AreaState.generating,
                    ),
                ),
                rx.chakra.hstack(
                    rx.chakra.text("A:", padding_x="8px", as_="b"),
                    rx.chakra.input(
                        value=question.answer,
                        on_change=lambda text: AreaState.update_answer(
                            question.id, text
                        ),
                        is_disabled=AreaState.generating,
                    ),
                ),
                
                align_items="left",
                spacing="4px",
                width="100%",
            ),
            rx.chakra.button(
                    rx.chakra.icon(tag="delete", size="24px"),
                    bg="red.100",
                    color="white",
                    _hover={"bg": "red.300"},
                    on_click=lambda: AreaState.delete_question(question.id),
                    width="40px",
                    height="40px",
                    align="right",
                    # position="absolute",
                    # right="8px",
                ),
            width="100%",
            height="auto",
        )
    )


@rx.page(route="/properties/[property_id]/edit/new_area")
def new_area_page() -> rx.Component:
    """A form to add new area"""
    return apply_layout(
        rx.chakra.vstack(
            rx.chakra.heading("Add a new area", size="2xl", padding="32px"),
            rx.chakra.hstack(
                rx.chakra.box(
                    rx.chakra.vstack(
                        rx.chakra.form_label("Name"),
                        rx.chakra.input(
                            placeholder="Name of the area",
                            name="name",
                            on_change=AreaState.update_name,
                        ),
                        rx.chakra.form_label(
                            "A short description of the area (Where are we? What is this area about?)"
                        ),
                        rx.text_area(
                            placeholder="Description",
                            name="desc",
                            rows="3",
                            on_change=AreaState.update_desc,
                        ),
                        rx.chakra.form_label("Video"),
                        rx.cond(
                            AreaState.video_url == "",
                            upload_zone(),
                            rx.video(
                                url=AreaState.video_url,
                                width="900px",
                                height="500px",
                            ),
                        ),
                        rx.chakra.spacer(),
                        rx.chakra.button(
                            "Save Area and Continue",
                            bg="blue",
                            color="white",
                            align="right",
                            is_disabled=AreaState.video_url == "",
                            on_click=AreaState.create_area,
                        ),
                        padding="8px",
                        spacing="16px",
                        align_items="left",
                        align="scretch",
                    ),
                    width="50%",
                    padding="32px",
                ),
                rx.chakra.card(
                    rx.chakra.vstack(
                        rx.chakra.heading("FAQ"),
                        rx.chakra.text(
                            "Add frequent questions that a visitor might ask so the AI assistant can answer them"
                        ),
                        rx.chakra.hstack(
                            rx.chakra.button(
                                "Add a question",
                                width="300px",
                                on_click=lambda: AreaState.add_question(
                                    "New question", "New answer"
                                ),
                            ),
                            rx.chakra.button(
                                "Suggest Questions",
                                bg="orange.400",
                                color="white",
                                align="right",
                                on_click=AreaState.suggest_faq,
                                width="300px",
                            ),
                            spacing="16px",
                        ),
                        rx.cond(
                            AreaState.generating,
                            rx.chakra.spinner(label="Generating questions..."),
                            rx.foreach(AreaState.questions.data.reverse(), qa_item),
                        ),
                        align_items="left",
                        spacing="16px",
                    ),
                    width="50%",
                    padding="32px",
                    height="100%",
                ),
                align_items="top",
            ),
            width="100%",
            height="100%",
            align_items="left",
        )
    )
