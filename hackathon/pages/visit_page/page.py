from hackathon.components.layout import apply_layout
import reflex as rx
from typing import List

from hackathon.pages.visit_page import area_selector, chat, media


def visit():
    return (
    apply_layout(
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
    ),
)