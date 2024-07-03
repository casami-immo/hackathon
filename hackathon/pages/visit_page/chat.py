import reflex as rx

from hackathon.components import loading_icon
from hackathon.pages.visit_page.state import QA, VisitState


message_style = dict(
    display="inline-block",
    padding="1em",
    border_radius="8px",
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
)


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.box(
            rx.markdown(
                qa.answer,
                background_color=rx.color("accent", 4),
                color=rx.color("accent", 12),
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(rx.foreach(VisitState.chat_history, message), width="100%"),
        padding_y="8px",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="8px",
        align_self="center",
        overflow="auto",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.box(
        rx.chakra.form(
            rx.chakra.form_control(
                rx.chakra.hstack(
                    rx.chakra.text_area(
                        placeholder="Ask question here",
                        name="question",
                        width="100%",
                        height="auto",
                        min_height="80px",
                        max_height="200px",
                        overflow_y="auto",
                        resize="vertical",
                    ),
                    rx.button(
                        rx.cond(
                            VisitState.processing,
                            loading_icon(height="1em"),
                            rx.text("Send"),
                        ),
                        type="submit",
                        height="40px",
                    ),
                    align_items="stretch",
                    width="100%",
                    padding="8px",
                ),
                is_disabled=VisitState.processing,
            ),
            on_submit=VisitState.process_question,
            reset_on_submit=True,
        ),
        padding="4",
        width="100%",
        align_items="center",
    )
