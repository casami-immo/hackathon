import reflex as rx
import reflex as rx
from backend.database import db
from backend.document_processing import extract_data
from hackathon.components.layout import apply_layout
from backend.models import Property


class FormState(rx.State):
    """The form state."""
    processing : bool = False
    # def handle_submit(self, form_data: dict):
    #     """Handle the form submit."""
    #     property_id = db.new_property(form_data)
    #     return rx.redirect(f"/properties/{property_id}/edit")

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        self.processing = True
        yield
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
        self.processing = False
        yield rx.redirect(f"/properties/{property_id}/edit")

def file_card(file: rx.UploadFile) -> rx.Component:
    return rx.chakra.hstack(
        rx.icon('circle-check'),
        rx.chakra.text(file),
        align_items='center',
    )


def new_property_from_document() -> rx.Component:
    return rx.chakra.form(
        rx.chakra.heading(
            "Import all the required documents to initialize all information in a minute",
            size="md",
        ),
        rx.chakra.vstack(
            rx.chakra.text("Required diagnostics: Carrez, DPE, Electricity"),
            rx.chakra.text("Optional: Taxes, Condo Fees"),
            rx.upload(
                rx.text("Drag and drop diagnostic files here or click to select files"),
                id="upload_diag",
                border="1px dotted rgb(107,99,246)",
                padding="5em",
                disabled=FormState.processing,
            ),
            rx.chakra.card(
                rx.chakra.grid(rx.foreach(rx.selected_files("upload_diag"), file_card)),
                header="Selected files",
                height="auto",
            ),
            rx.chakra.button(
                "Upload",
                on_click=FormState.handle_upload(
                    rx.upload_files(upload_id="upload_diag")
                ),
                is_loading=FormState.processing,
                bg="indigo",
                color="white",
                width="300px"
            ),
            align_items="left",
            spacing="16px",
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
                "Create new property",
                size="2xl",
            ),
            rx.chakra.box(height="32px"),
            # new_property_form(),
            new_property_from_document(),
            spacing="16px",
            align_items="left",
            padding="32px",
        )
    )
