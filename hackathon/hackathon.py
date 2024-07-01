"""The main Chat app."""

import reflex as rx
from hackathon.components import chat, navbar, media


def index() -> rx.Component:
    """The main app."""
    return (
        rx.vstack(
            rx.box(navbar(), width="100%"),
            rx.hstack(
                rx.box(
                    rx.video(
                        url="https://firebasestorage.googleapis.com/v0/b/hackathon-lablab.appspot.com/o/IMG_1906%20copie.MP4?alt=media&token=2fe0301b-ac23-4de7-a6f0-9c310b96806f",
                        width="100%",
                        height="100%",
                    ),
                    width="70%",
                    height="100%",
                    background_color=rx.color("white", 1),
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

    return rx.chakra.vstack(
        navbar(),
        rx.chakra.hstack(
            rx.box(
                rx.aspect_ratio(
                    rx.video(
                        url="https://www.youtube.com/embed/9bZkp7q19f0",
                        width="100%",
                        height="100%",
                    ),
                ),
                width="100%",
                height="100%",
            ),
            rx.chakra.vstack(
                chat.chat(),
                chat.action_bar(),
                background_color=rx.color("mauve", 1),
                color=rx.color("mauve", 12),
                min_height="100vh",
                align_items="stretch",
                spacing="0",
                width="40%",
                height="100%",
            ),
            width="100%",
            height="100%",
        ),
        width="100%",
        height="100%",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        background_color="gray",
        accent_color="indigo",
    ),
)
app.add_page(index)
