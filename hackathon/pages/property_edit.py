import reflex as rx
from backend.database import db

from hackathon.components.layout import apply_layout
import json

from backend.models import Area, Property


class PropEditState(rx.State):

    @rx.var
    def current_property(self) -> Property:
        try:
            property = db.get_property(self.router.page.params["property_id"])
        except KeyError:
            property = Property()
        return property

    @rx.var
    def areas(self) -> list[Area]:
        try:
            areas = db.list_areas(self.router.page.params["property_id"])
        except KeyError:
            areas = []
        return areas

    @rx.var
    def floor(self) -> str:
        return str(self.current_property.floor)

    @rx.var
    def surface(self) -> str:
        if self.current_property.diagnostics is None:
            return None
        return str(self.current_property.diagnostics.carrez.total)

    def new_area(self):
        return rx.redirect(
            f"/properties/{self.router.page.params['property_id']}/edit/new_area"
        )
    
    def delete_area(self, area_id: str):
        db.delete_area(self.router.page.params["property_id"], area_id)


def area_item(area: Area) -> rx.Component:
    return rx.chakra.vstack(
        rx.chakra.heading(area.name, size="xl", padding="4px"),
        rx.box(
            rx.video(url=area.video_url, width="300px", height="300px"),
        ),
        rx.chakra.button("Delete", on_click=PropEditState.delete_area(area.id)),
        padding="lg",
        align_items="left",
    )


def property_edit() -> rx.Component:
    return rx.cond(
        PropEditState.current_property.address == "",
        rx.chakra.heading("Property not found", size="2xl"),
        apply_layout(
            rx.chakra.vstack(
                rx.chakra.heading("Edit Property", size="2xl"),
                # display the property info
                rx.chakra.heading("Property Info", size="xl"),
                rx.chakra.text("Address: " + PropEditState.current_property.address),
                rx.chakra.text("Floor: " + PropEditState.floor),
                rx.chakra.text("Surface: " + PropEditState.surface),
                # display the areas
                rx.chakra.heading("Areas", size="xl"),
                rx.chakra.button(
                    "Add Area",
                    on_click=PropEditState.new_area,
                ),
                rx.foreach(PropEditState.areas, area_item),
                align_items="left",
            )
        ),
    )
