import reflex as rx
from backend.database import in_memory as db


class Property(rx.Base):
    """A property object."""
    name: str
    id: str

class PageState(rx.State):
    """The app state."""

    @rx.var
    def list_properties(self) -> list[Property]:
        """Get the list of properties."""
        properties = db.list_properties()
        return properties

def property_item(property: Property) -> rx.Component:
    """A property item."""
    return rx.chakra.box(
        rx.chakra.heading(property.name, size="xl", padding="4px"),
        rx.chakra.button("Visit", on_click=rx.redirect(f"/visit/{property.id}")),
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
