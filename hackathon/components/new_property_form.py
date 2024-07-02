import reflex as rx
from backend.database import in_memory as db


class FormState(rx.State):
    """The form state."""

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        property_id = db.new_property(form_data)
        print(property_id)
        rx.redirect(f"/properties/{property_id}/diagnostics")


def new_property_form() -> rx.chakra.Component:
    """The new property form."""
    return rx.chakra.vstack(
        rx.chakra.form(
            rx.chakra.vstack(
                rx.chakra.heading("Address", size="xl", padding="4px"),
                rx.chakra.input(
                    placeholder="Address", name="address", padding="4px"
                ),
                rx.chakra.heading("Property type", size="xl", padding="4px"),

                rx.chakra.radio_group(
                    ["appartment", "house"], default_value="appartment", name="type"
                ),
                rx.chakra.heading("Floor", size="xl", padding="4px"),

                rx.chakra.number_input(
                    placeholder="Let 0 for house",
                    name="floor",
                    type="integer",
                ),

                rx.chakra.heading("Surface", size="xl", padding="4px"),
                rx.chakra.number_input(
                    placeholder="m2",
                    name="surface",
                    type="integer",
                ),
                # rx.chakra.heading("Documents", size="xl", padding="4px"),
                # rx.chakra.upload("Upload mandatory documents", name="documents", multiple=True),

                rx.chakra.button("Submit", type_="submit"),
                width="50vw",
                height="100%",
                align_items="left"
            ),
            
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
    )
