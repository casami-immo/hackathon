import os
import copy
from typing import List, Tuple
from openai import OpenAI
import reflex as rx
from .database import db


# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


def get_property_info(property_id: str) -> Tuple[str, str]:
    """Get the property information from the database."""
    property_info = db.get_property(property_id).dict()

    # remove video url and subtitles in areas
    for id_, area in property_info["areas"].items():
        area.pop("video", None)
        area.pop("subtitles", None)
        property_info["areas"][id_] = area
    return property_info

class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

SYSTEM_PROMPT = """
You are a AI real estate agent called Casami. You are guiding the user to visit a property in a virtual tour.
Answer the user questions about the property in a professional manner. 
Always based your answers on the information provided, do not make up information. 
If the information is not available, say that you do not have that information and you will contact the owner and get back to them.

"""

async def answer(question: str, chat_history=List[QA], context: str = None):
    "Call OPENAI API to get the answer, yielding the response token by token."
    # Build the messages.

    property_id = context.get("property_id")

    prompt = SYSTEM_PROMPT
    if property_id is not None:
        property_info = get_property_info(property_id)
        prompt += f"Current Property information:\n{property_info}\nCurrent Area the user is seeing: {context.get('current_area')}\n\n"

    messages = [
        {
            "role": "system",
            "content": prompt,
        }
    ]
    for qa in chat_history:
        messages.append({"role": "user", "content": qa.question})
        messages.append({"role": "assistant", "content": qa.answer})

    # Remove the last mock answer.
    messages.pop(-1)

    session = session = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=messages,
            stream=True,
            temperature=0.1,
        )
    for item in session:
        if hasattr(item.choices[0].delta, "content"):
            answer_text = item.choices[0].delta.content
            yield answer_text