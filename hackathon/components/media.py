import reflex as rx

from hackathon.state import State


def video() -> rx.Component:
    """A video player."""
    return rx.video(
            src="https://www.youtube.com/embed/9bZkp7q19f0",
            width="50vw",
            height="50vw",
        ),
