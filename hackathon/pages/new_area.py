import reflex as rx
from hackathon.components.layout import apply_layout
from backend.database import db
from backend.models import Area

class AreaState(rx.State):
    """The app state."""

    video = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.video = f"http://localhost:8000/_upload/{file.filename}"

    @rx.var
    def video_uploaded(self):
        return self.video != ""

    def create_area(self, form_data: dict):
        """Create a new area."""
        db.add_area(
            property_id=self.router.page.params["property_id"],
            area=Area(
                name=form_data["name"],
                description=form_data["desc"],
                video_url=self.video,
                qa=[],
            )
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
                    AreaState.video_uploaded,
                    rx.video(url=AreaState.video, width="500px", height="300px"),
                    upload_zone(),
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
