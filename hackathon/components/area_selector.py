import reflex as rx
from hackathon.state import State

def next_area_button() -> rx.Component:
    """The next area button."""
    return rx.button(
        "Next",
        on_click=lambda: State.next_area,
    )

def previous_area_button() -> rx.Component:
    """The previous area button."""
    return rx.button(
        "Previous",
        on_click=lambda: State.previous_area,
    )

def select_area_dropdown() -> rx.Component:
    """The select area dropdown."""
    return rx.select(
        items=State.areas_names,
        value=State.current_area_name,
        on_change=State.switch_area,
    )

def area_selector_panel() -> rx.Component:
    """The area selector panel."""
    return rx.hstack(
        
        previous_area_button(),
        select_area_dropdown(),
        next_area_button(),
        align="stretch",
    )