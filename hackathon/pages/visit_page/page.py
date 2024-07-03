from hackathon.components.layout import apply_layout
import reflex as rx
from typing import List

from hackathon.pages.visit_page import area_selector, chat, media


def visit():
    return (
    apply_layout(
        rx.chakra.box(
            rx.chakra.hstack(
                rx.chakra.box(
                    rx.chakra.vstack(
                        rx.chakra.box(
                            area_selector.area_selector_panel(),
                            width="100%",
                            padding="8px",
                            align_items="center",
                            background_color="gray",
                        ),
                        rx.chakra.box(
                            media.video(),
                            width="100%",
                            height="1000px",
                        ),
                    ),
                    height="100%",
                    flex=1,
                    background_color="white",
                ),
                rx.chakra.box(
                    rx.chakra.vstack(
                        chat.chat(),
                        chat.action_bar(),
                        align_items="stretch",
                        spacing="0",
                        height="100%",  
                    ),
                    width="500px",
                    height="100%",
                    background_color=rx.color("indigo", 2),
                ),
                width="100%",
                height="100%",
            ),
            width="100%",
            height="100%",
            bg="gray",
            padding="4px"
        ),
    ),
)