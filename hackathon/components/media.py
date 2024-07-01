import reflex as rx

from hackathon.state import State


def video() -> rx.Component:
    """A video player."""
    return (
        rx.video(
            url=State.video_url,
            width="100%",
            height="100%",
        ),
    )
