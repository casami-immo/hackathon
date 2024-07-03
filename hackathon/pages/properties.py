import reflex as rx

from typing import List
import logging

from backend.database import db
from backend.models import Property


class PageState(rx.State):
    """The app state."""

    @rx.var
    def list_properties(self) -> List[Property]:
        """Get the list of properties."""
        properties = db.list_properties()
        logging.info("Loaded %s properties", len(properties))
        return properties

    def delete_property(self, property_id: str):
        """Delete the property."""
        db.delete_property(property_id)


def property_item(property: Property) -> rx.Component:
    """A property item."""
    return rx.chakra.card(
        rx.chakra.vstack(
            rx.chakra.heading(property.name, size="lg", padding="4px"),
            rx.chakra.box(
                rx.chakra.hstack(
                    rx.chakra.button(
                        "Visit",
                        on_click=rx.redirect(f"/visit/{property.id}"),
                        bg="coral",
                        color="white",
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.button(
                        "Edit", on_click=rx.redirect(f"/properties/{property.id}/edit")
                    ),
                    rx.chakra.button(
                        "Delete",
                        on_click=PageState.delete_property(property.id),
                        bg=rx.color("red", 10),
                        color="white",
                    ),
                    align_items="right",
                    width="100%",
                    height="100%",
                    spacing="16px",
                ),
                position="absolute",
                bottom="8px",
                right="8px",
                left="8px"
            ),
            width="500px",
            height="150px",
            padding="4px",
            align_items="left",
        ),
        width="500px",
        height="200px",
    )


def properties() -> rx.Component:
    """List the properties."""
    return rx.chakra.vstack(
        rx.chakra.heading("Properties", size="2xl", align="left"),
        rx.box(height="32px"),
        rx.chakra.button(
            "New Property",
            on_click=rx.redirect("/new_property"),
            width="160px",
            padding="4px",
            bg="blue",
            color="white",
        ),
        rx.spacer(height="16px"),
        rx.foreach(PageState.list_properties, property_item, spacing="8px"),
        align_items="left",
        width="100%",
        padding="64px",
    )
