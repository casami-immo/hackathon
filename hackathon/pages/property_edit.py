import reflex as rx
from backend.database import in_memory as db

from hackathon.components.layout import apply_layout
import json


class Area(rx.Base):
    """An area object."""

    name: str
    id: str
    video: str

class PropertyInfo(rx.Base):
    """A property object."""

    name: str
    id: str
    address: str
    floor: str
    surface: str
    areas: list[Area]


class PropEditState(rx.State):

    @rx.var
    def current_property(self) -> PropertyInfo:
        try:
            property = db.get_property_by_id(self.router.page.params["property_id"])
            property["surface"] = str(property["diagnostics"]["carrez"]["total"])
        except KeyError:
            property = {}
        return property
    
    @rx.var
    def areas(self) -> list[Area]:
        try:
            property = db.get_property_by_id(self.router.page.params["property_id"])
            areas = property["areas"]
        except KeyError:
            areas = []
        return areas
    
    def new_area(self):
        return rx.redirect(f"/properties/{self.router.page.params['property_id']}/edit/new_area")

def area_item(area: Area) -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.heading(area.name, size="xl", padding="4px"),
        rx.box(
            rx.video(url=area.video, width="300px", height="300px"),
        ),
        padding="lg",
        align_items="left",
    )

def property_edit() -> rx.Component:
    return apply_layout(
        rx.chakra.vstack(
            rx.chakra.heading("Edit Property", size="2xl"),
            # display the property info
            rx.chakra.heading("Property Info", size="xl"),

            rx.chakra.text(
                "Address: " + PropEditState.current_property.address
            ),
            rx.chakra.text(
                "Floor: " + PropEditState.current_property.floor
            ),
            rx.chakra.text(
                "Surface: " + PropEditState.current_property.surface
            ),
            # display the areas
            rx.chakra.heading("Areas", size="xl"),
            rx.chakra.button(
                "Add Area", 
                on_click=PropEditState.new_area,
            ),
            rx.foreach(PropEditState.areas, area_item),
            align_items="left",
        )
    )
