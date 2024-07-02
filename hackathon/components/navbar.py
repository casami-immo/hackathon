import reflex as rx


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.avatar(fallback="C", variant="solid"),
                rx.heading("Virtual Visit with Casami"),
                # rx.desktop_only(
                #     rx.badge(
                #     State.current_chat,
                #     rx.tooltip(rx.icon("info", size=14), content="The current selected chat."),
                #     variant="soft"
                #     )
                # ),
                align_items="center",
            ),
            # rx.hstack(
            #     modal(rx.button("+ New chat")),
            #     sidebar(
            #         rx.button(
            #             rx.icon(
            #                 tag="messages-square",
            #                 color=rx.color("mauve", 12),
            #             ),
            #             background_color=rx.color("mauve", 6),
            #         )
            #     ),
            #     rx.desktop_only(
            #         rx.button(
            #             rx.icon(
            #                 tag="sliders-horizontal",
            #                 color=rx.color("mauve", 12),
            #             ),
            #             background_color=rx.color("mauve", 6),
            #         )
            #     ),
            #     align_items="center",
            # ),
            justify_content="space-between",
            align_items="center",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        padding="12px",
        border_bottom=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        position="sticky",
        top="0",
        z_index="100",
        align_items="center",
    )
