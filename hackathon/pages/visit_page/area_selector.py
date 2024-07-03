import reflex as rx
from hackathon.pages.visit_page.state import VisitState

def next_area_button() -> rx.Component:
    """The next area button."""
    return rx.button(
        "Next",
        on_click=lambda: VisitState.next_area,
    )

def previous_area_button() -> rx.Component:
    """The previous area button."""
    return rx.button(
        "Previous",
        on_click=lambda: VisitState.previous_area,
    )

def select_area_dropdown() -> rx.Component:
    """The select area dropdown."""
    return rx.select(
        items=VisitState.areas_names,
        value=VisitState.current_area_name,
        on_change=VisitState.switch_area,
    )

def area_selector_panel() -> rx.Component:
    """The area selector panel."""
    return rx.chakra.hstack(
        previous_area_button(),
        select_area_dropdown(),
        next_area_button(),
        align="stretch",
        spacing="32px",
        align_items="center",
        width="100%",
    )