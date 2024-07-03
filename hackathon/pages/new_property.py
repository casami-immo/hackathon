import reflex as rx
import reflex as rx
from backend.database import db
from backend.document_processing import extract_data
from hackathon.components.layout import apply_layout
from backend.models import Property

class FormState(rx.State):
    """The form state."""

    # def handle_submit(self, form_data: dict):
    #     """Handle the form submit."""
    #     property_id = db.new_property(form_data)
    #     return rx.redirect(f"/properties/{property_id}/edit")

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        outfiles = []
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            outfiles.append(outfile)

        # Process info
        property = extract_data(outfiles)
        print(property)
        # Save the data
        property_id = db.add_property(property)
        # wait and check if the property is saved
        # if not, return error message
        # if saved, redirect to the edit page
        property_check = db.get_property(property_id)
        return rx.redirect(f"/properties/{property_id}/edit")


def new_property_from_document() -> rx.Component:
    return rx.chakra.form(
        rx.chakra.heading(
            "Import information from Diagnostics", size="2xl", padding="4px"
        ),
        rx.upload(
            rx.text("Drag and drop diagnostic files here or click to select files"),
            id="upload_diag",
            border="1px dotted rgb(107,99,246)",
            padding="5em",
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload_diag"), rx.text)),
        rx.chakra.button(
            "Upload",
            on_click=FormState.handle_upload(rx.upload_files(upload_id="upload_diag")),
        ),
        width="50vw",
        height="100%",
        align_items="left",
        spacing="16px",
    )


# def new_property_form() -> rx.chakra.Component:
#     """The new property form."""
#     return rx.chakra.vstack(
#         rx.chakra.form(
#             rx.chakra.vstack(
#                 rx.chakra.heading("Address", size="xl", padding="4px"),
#                 rx.chakra.input(placeholder="Address", name="address", padding="4px"),
#                 rx.chakra.heading("Property type", size="xl", padding="4px"),
#                 rx.chakra.radio_group(
#                     ["appartment", "house"], default_value="appartment", name="type"
#                 ),
#                 rx.chakra.heading("Floor", size="xl", padding="4px"),
#                 rx.chakra.number_input(
#                     placeholder="Let 0 for house",
#                     name="floor",
#                     type="integer",
#                 ),
#                 rx.chakra.heading("Surface", size="xl", padding="4px"),
#                 rx.chakra.number_input(
#                     placeholder="m2",
#                     name="surface",
#                     type="integer",
#                 ),
#                 # rx.chakra.heading("Documents", size="xl", padding="4px"),
#                 # rx.chakra.upload("Upload mandatory documents", name="documents", multiple=True),
#                 rx.chakra.button("Submit", type_="submit"),
#                 width="50vw",
#                 height="100%",
#                 align_items="left",
#             ),
#             on_submit=FormState.handle_submit,
#             reset_on_submit=True,
#         ),
#     )


def new_property() -> rx.Component:
    """The new property page."""
    return apply_layout(
        rx.chakra.vstack(
            rx.chakra.heading(
                "Add new property",
                size="2xl",
            ),
            # new_property_form(),
            new_property_from_document(),
            spacing="16px"
        )
    )