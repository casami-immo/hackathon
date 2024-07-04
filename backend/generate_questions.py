import base64
import os
from io import BytesIO
from typing import List

import cv2
import google.generativeai as genai
import requests
from google.ai import generativelanguage as glm
from PIL import Image


def get_sys_prompt(name_area, description, questions):
    prefix = f"""
    Role: AI Assistant for Property Buyers

    Context:
    You are an AI designed to help potential property buyers formulate relevant questions based on video tours of different areas of a property. Your goal is to assist buyers in gathering comprehensive information to make informed decisions.

    Input:
    - {name_area}: The specific area of the property being discussed (e.g., kitchen, living room, garden)
    - Brief description of the area: {description}
    - Video content: The frames images of video tour of the {name_area}

    Task:
    Generate a list of pertinent questions a potential buyer should ask the seller or real estate agent about the {name_area}, based on the video tour.

    Instructions:
    1. Analyze the provided video content for the {name_area}.
    2. Identify key features, potential concerns, and points of interest that a buyer should inquire about.
    3. Formulate at least 5 specific, relevant questions about the {name_area}.
    4. Ensure questions cover various aspects such as:
    - Condition and age of fixtures/appliances
    - Recent renovations or needed repairs
    - Unique features or potential issues
    - Practical considerations (e.g., storage, functionality)
    - Any aspects not clearly visible or explained in the video

    Output Format:
    Provide a numbered list of questions (minimum 5) without additional commentary. Each question should:
    - Be clear and concise
    - Focus on a single aspect of the {name_area}
    - Provide valuable information for a potential buyer's decision-making process
    - Some questions can be relevant to the frame images of the video tour

    Note: Adapt your questions to the specific features and potential concerns relevant to the {name_area} being discussed.

    Example Output:
    """
    qa_info = f"""{questions}"""
    return prefix + qa_info


def download_video(url, filename):
    response = requests.get(url, stream=True, timeout=30)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Video downloaded successfully: {filename}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")


def read_videos(video_path, fmt="PNG", interval_seconds=1):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    video = cv2.VideoCapture(video_path)

    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval_seconds)

    frame_count = 0
    base64_images = []
    while frame_count < total_frames:
        success, frame = video.read()

        if not success:
            break

        if frame_count % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            pil_image = pil_image.resize((512, 512))

            buffered = BytesIO()
            pil_image.save(buffered, format=fmt)

            base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_images.append(base64_str)
        frame_count += 1
    video.release()
    return base64_images, total_frames // fps


def suggest_questions(
    name: str, description: str, video_url: str, current_questions: List[str]
):
    """
    Generate questions based on the video content and description of the area.
    Args:
        name (str): The name of the area.
        description (str): The description of the area.
        video_url (str): The URL of the video content.
        current_questions (list(str)): The current list of questions for the area.
    Returns:
    questions (list(str)): Max 5 generated questions.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    video_local_path = os.path.join(current_dir, f"/videos/{name}.mp4")
    download_video(video_url, video_local_path)
    base64_images, _ = read_videos(video_local_path)
    system_prompt = get_sys_prompt(name, description, current_questions)
    model = genai.GenerativeModel(
        "gemini-1.5-flash-latest", system_instruction=[system_prompt]
    )
    parts = []
    for image in base64_images:
        parts.append(glm.Blob(mime_type="image/png", data=image))

    messages = [{"role": "user", "parts": parts}]

    response = model.generate_content(
        messages, generation_config={"response_mime_type": "application/json"}
    )
    response_text = response.candidates[0].content.parts[0].text
    if isinstance(response_text, str):
        questions = response_text.split("\n")
        questions = [question.strip() for question in questions]
    elif isinstance(response_text, list):
        questions = [question.strip() for question in response_text]
    else:
        questions = []
    return questions[:5]
