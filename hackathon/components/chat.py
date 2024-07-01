import reflex as rx

from hackathon.components import loading_icon
from hackathon.state import QA, State, ChatState


message_style = dict(display="inline-block", padding="1em", border_radius="8px", max_width=["30em", "30em", "50em", "50em", "50em", "50em"])


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
        rx.box(rx.foreach(ChatState.chat_history, message), width="100%"),
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.box(
        rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        rx.radix.text_field.root(
                            rx.radix.text_field.input(
                                placeholder="Ask question here",
                                id="question",

                                # width=["15em", "20em", "45em", "50em", "50em", "50em"],
                            ),
                            # rx.radix.text_field.slot(
                            #     rx.tooltip(
                            #         rx.icon("info", size=18),
                            #         content="Enter a question to get a response.",
                            #     )
                            # ),
                            width="100%",
                            height="40px",
                        ),
                        rx.button(
                            rx.cond(
                                ChatState.processing,
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
                    is_disabled=ChatState.processing,
                ),
                on_submit=ChatState.process_question,
                reset_on_submit=True,
            ),
        padding="4",
        width="100%",
        align_items="center",
    )
