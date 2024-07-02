"""The main Chat app."""

import reflex as rx
from hackathon.components.layout import apply_layout
from hackathon.pages.new_property import new_property
from hackathon.pages.properties import properties
from hackathon.pages.visit_page.page import visit

def index() -> rx.Component:
    """The main app."""
    return(
        apply_layout(
            properties()
        )
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        background_color="white",
        accent_color="indigo",
    ),
)
app.add_page(index)
# app.add_page(new_property, route="/new_property")
app.add_page(visit, route="/visit/[property_id]")
