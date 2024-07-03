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
    return rx.chakra.box(
        rx.chakra.heading(property.name, size="xl", padding="4px"),
        rx.chakra.button("Visit", on_click=rx.redirect(f"/visit/{property.id}")),
        rx.chakra.button("Edit", on_click=rx.redirect(f"/properties/{property.id}/edit")),
        rx.chakra.button("Delete", on_click=PageState.delete_property(property.id)),
        width="100%",
        padding="lg",
    )

def properties() -> rx.Component:
    """List the properties."""
    return rx.chakra.vstack(
        rx.chakra.heading("Properties", size="2xl", padding="4px"), 
        rx.chakra.button("New Property", on_click=rx.redirect("/new_property")),
        rx.foreach(PageState.list_properties, property_item),  
    )
