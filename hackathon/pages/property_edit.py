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
            if property is None:
                return Property()
        except KeyError:
            property = Property()
        return property

    @rx.var
    def areas(self) -> list[Area]:
        try:
            areas = db.list_areas(self.router.page.params["property_id"])
            for area in areas:
                area.video.url = area.video.url.replace(
                    "http://localhost:8000/", f"http://{self.router.headers.host}/"
                )
        except KeyError:
            areas = []
        return areas

    @rx.var
    def floor(self) -> str:
        try:
            return str(self.current_property.floor)
        except:
            return "unknown"

    @rx.var
    def surface(self) -> str:
        if self.current_property.diagnostics is None:
            return "unknown"
        return str(self.current_property.diagnostics.carrez.total)

    def new_area(self):
        return rx.redirect(
            f"/properties/{self.router.page.params['property_id']}/edit/new_area"
        )

    def delete_area(self, area_id: str):
        db.delete_area(self.router.page.params["property_id"], area_id)


def area_item(area: Area) -> rx.Component:
    return rx.chakra.card(
        rx.chakra.vstack(
            rx.chakra.hstack(
                rx.chakra.heading(area.name, size="lg", padding_y="16px"),
                rx.chakra.spacer(),
                rx.chakra.hstack(
                    rx.chakra.button(
                        "Delete", on_click=PropEditState.delete_area(area.id),
                        bg="red.100",
                        color="white",
                        _hover={"bg": "red.500"},
                    ),
                    rx.chakra.button(
                        "Edit",
                        on_click=rx.redirect(
                            f"/properties/{PropEditState.current_property.id}/areas/{area.id}/caption"
                        ),
                    ),
                ),
            ),
            rx.box(
                rx.video(url=area.video.url, width="500px", height="300px"),
            ),
            padding="lg",
            align_items="left",
        ),
        width="900px",
        height="400px",
    )


def property_edit() -> rx.Component:
    return rx.cond(
        PropEditState.current_property.address == "",
        rx.chakra.vstack(
            rx.chakra.heading("Property not found", size="2xl"),
            rx.chakra.button(
                "Go back",
                on_click=rx.redirect("/"),
            ),
            spacing="32px",
            align="center",
            align_items="center",
            padding="64px",
        ),
        apply_layout(
            rx.chakra.vstack(
                rx.chakra.heading("Edit Property", size="2xl", padding_y="32px"),
                # display the property info
                rx.chakra.heading("Property Info", size="xl"),
                rx.chakra.text("Address: " + PropEditState.current_property.address),
                rx.chakra.text("Floor: " + PropEditState.floor),
                rx.chakra.text("Surface: " + PropEditState.surface),
                rx.chakra.button(
                    "Save property and go back",
                    on_click=rx.redirect(f"/"),
                    bg="green.100",
                    width="350px",
                ),
                # display the areas
                rx.box(height="32px"),
                rx.chakra.heading("Areas", size="xl"),
                rx.text("Areas are different zones in property for visit"),
                rx.chakra.button(
                    "Add new area",
                    on_click=PropEditState.new_area,
                    bg="indigo",
                    color="white",
                    width="350px",
                ),
                rx.foreach(PropEditState.areas, area_item),
                align_items="left",
                padding="64px",
            )
        ),
    )
