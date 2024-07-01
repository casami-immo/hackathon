import os
from typing import List, Tuple
from openai import OpenAI
import reflex as rx


# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


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
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
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