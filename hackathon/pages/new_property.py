import reflex as rx
from hackathon.components.new_property_form import new_property_form


def new_property() -> rx.Component:
    """The new property page."""
    return rx.chakra.container(
        rx.vstack(
        rx.chakra.heading("Add new property", size="2xl", ),
        new_property_form(),
        ),
        max_width="50vw",
        padding="32px",
        align_items="center",
    )