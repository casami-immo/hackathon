import reflex as rx

from hackathon.pages.visit_page.state import QA, VisitState


def video() -> rx.Component:
    """A video player."""
    return (
        rx.video(
            url=VisitState.video_url,
            width="100%",
            height="100%",
        ),
    )
