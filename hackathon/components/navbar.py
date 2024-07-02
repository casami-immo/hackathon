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
            # Link to the home page.
            rx.link("Home", on_click=rx.redirect("/"), variant="soft", padding="12px"),
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
