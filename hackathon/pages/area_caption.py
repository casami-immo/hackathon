import reflex as rx
from hackathon.components.layout import apply_layout

from backend.database import db
from backend.models import Area, File
from backend.generate_video_with_audio import (
    generate_descriptions,
    merge_caption_to_video,
)
from uuid import uuid4

class AreaCaptionState(rx.State):
    """The app state."""

    generating: bool = False
    caption: str = ""
    output_file: File = File(filename="", url="")
    # output_video_url: str = ""

    @rx.var
    def output_video_url(self) -> str:
        """Get the output video URL."""
        try:
            if "localhost" in self.output_file.url:
                return self.output_file.url.replace(
                    "http://localhost:8000/", f"http://{self.router.headers.host}/"
                )
            else:
                return self.output_file.url
        except:
            return ""

    @rx.cached_var
    def area(self) -> Area:
        """Get the current area."""
        try:
            print(self.router.page.params)
            return db.get_area(
                self.router.page.params.get("property_id", "0"),
                self.router.page.params.get("area_id", "0")
            )
        except Exception as exc:
            raise exc
            return Area(name="")

    @rx.var
    def video_url(self) -> str:
        """Get the current video URL."""
        try:
            if "localhost" in self.area.video.url:
                return self.area.video.url.replace(
                    "http://localhost:8000/", f"http://{self.router.headers.host}/"
                )
            else:
                return self.area.video.url
        except:
            return ""

    async def generate_caption(self):
        """Generate the caption for the area."""
        self.generating = True
        yield
        try:
            # Generate the descriptions
            self.caption = ""
            for chunk in generate_descriptions(
                area=self.area, video_url=self.video_url
            ):
                self.caption += chunk
                yield
        finally:
            self.generating = False
            yield

    async def merge_caption_to_video(self):
        """Merge the caption to the video."""
        self.generating = True
        yield
        try:

            output_video_content = merge_caption_to_video(
                video_url=self.video_url,
                caption=self.caption,
            )
            id_ = db.add_file(
                filename=f"{uuid4()}.mp4", content=output_video_content
            )
            self.output_file = db.get_file(id_)
            print(self.output_file)
        finally:
            self.generating = False
            yield

    def update_caption(self, caption):
        """Update the caption."""
        self.caption = caption

    def save_area(self):
        """Save the area."""
        self.area.video = self.output_file
        db.update_area(
            self.router.page.params["property_id"],
            self.router.page.params["area_id"],
            self.area,
        )
        return rx.redirect(
            f"/properties/{self.router.page.params['property_id']}/edit")


@rx.page(route="/properties/[property_id]/areas/[area_id]/caption")
def area_caption():
    return apply_layout(
        rx.cond(
            AreaCaptionState.area.name == "",
            rx.chakra.heading("Area not found", size="xl", padding="4px"),
            rx.chakra.vstack(
                rx.chakra.heading("Edit Area Caption", size="2xl", padding="4px"),
                rx.chakra.heading(
                    "Area: " + AreaCaptionState.area.name, size="lg", padding="4px"
                ),
                rx.chakra.heading("Description", size="lg", padding="4px"),
                rx.text(AreaCaptionState.area.description),
                rx.chakra.heading("Video", size="lg", padding="4px"),
                rx.video(url=AreaCaptionState.video_url, width="300px", height="300px"),
                rx.chakra.vstack(
                    rx.chakra.heading(
                        "Add caption to the video", size="lg", padding="4px"
                    ),
                    rx.chakra.button(
                        "Generate Caption",
                        color_scheme="blue",
                        is_loading=AreaCaptionState.generating,
                        on_click=AreaCaptionState.generate_caption,
                    ),
                    rx.text_area(
                        label="Caption",
                        name="caption",
                        value=AreaCaptionState.caption,
                        on_change=AreaCaptionState.update_caption,
                        disabled=AreaCaptionState.generating,
                        size="3",
                        width="500px",
                        height="300px",
                    ),
                    rx.chakra.button(
                        "Turn into voice commentary",
                        color_scheme="blue",
                        is_loading=AreaCaptionState.generating,
                        on_click=AreaCaptionState.merge_caption_to_video,
                    ),
                    rx.cond(
                        AreaCaptionState.output_video_url != "",
                        rx.video(
                            url=AreaCaptionState.output_video_url,
                            width="300px",
                            height="300px",
                        ),
                        rx.box(width="0px", height="0px"),
                    ),
                    rx.chakra.button(
                        "Save Area", color="indigo", on_click=AreaCaptionState.save_area
                    ),
                    padding="4px",
                ),
                width="100%",
                height="100%",
            ),
        )
    )