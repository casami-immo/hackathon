"""The main Chat app."""

import reflex as rx
from hackathon.components import chat, navbar, media, area_selector
from hackathon.pages.new_property import new_property

def index() -> rx.Component:
    """The main app."""
    return (
        rx.vstack(
            rx.box(navbar(), width="100%"),
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.box(
                            area_selector.area_selector_panel(),
                            width="100%",
                            padding="8px",
                        ),
                        rx.box(
                            media.video(),
                            width="100%",
                            height="90%",
                        ),
                        width="100%",
                        height="100%",
                    ),
                    width="70%",
                    height="100%",
                    background_color=rx.color("white"),
                ),
                rx.box(
                    rx.chakra.vstack(
                        chat.chat(),
                        chat.action_bar(),
                        align_items="stretch",
                        spacing="0",
                        height="100%",
                    ),
                    width="30%",
                    height="100%",
                    background_color=rx.color("indigo", 12),
                ),
                width="100%",
                height="100%",
            ),
            width="100vw",
            height="94vh",
            spacing="0",
        ),
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
app.add_page(new_property, route="/new_property")