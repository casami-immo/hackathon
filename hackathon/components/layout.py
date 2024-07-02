import reflex as rx
from .navbar import navbar


def apply_layout(children):
    """Apply the layout."""
    return rx.chakra.vstack(
        rx.chakra.box(navbar(), width="100%"),
        children,
        width="100vw",
        height="100vh",
        spacing="0",
    )