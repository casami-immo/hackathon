import reflex as rx
from hackathon.components.layout import apply_layout
from backend.database import db
from backend.models import Area, File


class AreaState(rx.State):
    """The app state."""

    video_file_id = ""
    video_url = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()

            self.video_file_id = db.add_file(
                filename=file.filename,
                content=upload_data,
            )
            self.video_url = db.get_file(self.video_file_id).url

    def create_area(self, form_data: dict):
        """Create a new area."""
        db.add_area(
            property_id=self.router.page.params["property_id"],
            area=Area(
                name=form_data["name"],
                description=form_data["desc"],
                video=db.get_file(self.video_file_id),
                qa=[],
            ),
        )
        return rx.redirect(f"/properties/{self.router.page.params['property_id']}/edit")


def upload_zone():
    return rx.upload(
        rx.vstack(
            rx.button("Select File", bg="white"),
            rx.text("Drag and drop files here or click to select files"),
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


@rx.page(route="/properties/[property_id]/edit/new_area")
def new_area_page() -> rx.Component:
    """A form to add new area"""
    return apply_layout(
        rx.chakra.vstack(
            rx.chakra.heading("Add a new area"),
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.chakra.form_label("Name"),
                    rx.chakra.input(placeholder="Name of the area", name="name"),
                ),
                rx.chakra.form_control(
                    rx.chakra.form_label("A short description of the area"),
                    rx.chakra.input(placeholder="Description", name="desc"),
                ),
                rx.cond(
                    AreaState.video_url == "",
                    upload_zone(),
                    rx.video(url=AreaState.video_url, width="500px", height="300px"),
                ),
                rx.chakra.form_control(
                    rx.chakra.button("Save Area", color="indigo", type_="submit"),
                ),
                padding="lg",
                spacing="lg",
                on_submit=AreaState.create_area,
            ),
        )
    )
