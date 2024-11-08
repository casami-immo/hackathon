import base64
import os
from io import BytesIO
import tempfile

import cv2
import google.generativeai as genai
import requests
from google.ai import generativelanguage as glm
from moviepy.editor import (
    AudioClip,
    AudioFileClip,
    VideoFileClip,
    concatenate_audioclips,
)
from openai import OpenAI
from PIL import Image
from time import perf_counter
from backend.database import db


WORD_PER_MINUTE = 110


def download_video(url, filename):
    response = requests.get(url, stream=True, timeout=30)
    print(response.status_code)
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


def calculate_max_words(length):
    return int(WORD_PER_MINUTE / 60 * length)


def get_system_prompt(name_area, desctiption, qa_pairs, max_words=150):
    prefix = f"""
    Role: Expert Real Estate Agent

    Task: Create an engaging property description with max {max_words}-word based on a video tour and provided Q&A.

    Context:
    - You're presenting a property to potential buyers
    - You have access to a video tour of the building and its surroundings
    - Additional information is provided in a Q&A format

    Instructions:
    1. Analyze the video content and Q&A information
    2. Highlight key features of the building and its location
    3. Craft a compelling {max_words}-word-max description that:
    - Captures the essence of the property
    - Emphasizes its unique selling points
    - Incorporates relevant details from the Q&A
    - Uses vivid, professional language
    4. Always start with introducing that we are in {name_area}. For example: "we are entering the {name_area} area"
    5. Use the information from the description below to add information not present in the video or Q&A
        Description: {desctiption}

    Style Guide:
    - Tone: Enthusiastic and authoritative
    - Focus: Property strengths and locational advantages
    - Language: Clear, simple, concise, and persuasive

    Format: Continuous prose, ideally {max_words} words but don't repeat yourself.

    Note: Ensure the description flows naturally and engages potential buyers. Seamlessly integrate information from both the video and Q&A without explicitly referencing their source.

    Below are some information about the property:
    """
    qa_info = "\n".join([f"- {qa['question']}: {qa['answer']}" for qa in qa_pairs])
    return prefix + qa_info


def generate_descriptions(area, video_url):
    start = perf_counter()
    with tempfile.TemporaryDirectory() as path:
        video_path = os.path.join(path, "video.mp4")
        print(f'Downloading video {video_url}')
        download_video(video_url, video_path)
        print(perf_counter() - start)
        print('Reading video')
        base64_images, length = read_videos(video_path)
        print(perf_counter() - start)
    print("Preparing the prompt")
    name_area = area.name
    description = area.description
    qa_pairs = area.dict()["qa"]
    max_words = calculate_max_words(length)
    system_prompt = get_system_prompt(name_area, description, qa_pairs, max_words)
    model = genai.GenerativeModel(
        "gemini-1.5-flash-latest", system_instruction=[system_prompt]
    )
    parts = []
    for idx, image in enumerate(base64_images):
        parts.append(glm.Blob(mime_type="image/png", data=image))

    messages = [{"role": "user", "parts": parts}]
    # print(perf_counter() - start)
    print('Generating caption')
    response = model.generate_content(messages, stream=True)
    for chunk in response:
        try:
            yield chunk.text
        except Exception as e:
            continue

    # print(perf_counter() - start)


def text_to_speech_audio(text, audio_path):
    client = OpenAI()
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    response.stream_to_file(audio_path)


def combine_audio_video(audio_path, video_path, output_directory):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    silence = AudioClip(
        make_frame=lambda t: 0,
        duration=video_clip.duration - audio_clip.duration,
        fps=24,
    )

    audio_clip = concatenate_audioclips([audio_clip, silence])
    final_clip = video_clip.set_audio(audio_clip.subclip(0, video_clip.duration))
    output_file_name = (
        os.path.basename(video_path).split(os.path.extsep)[0] + "_with_audio.mp4"
    )

    output_file_path = os.path.join(output_directory, output_file_name)
    final_clip.write_videofile(
        output_file_path,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-crf", "18", "-aspect", "9:16"],)

    print(f"Combined video and audio file saved as {output_file_path}")
    return output_file_path


def merge_caption_to_video(video_url, caption):
    with tempfile.TemporaryDirectory() as path:
        audio_path = os.path.join(path, "caption.mp3")
        video_local_path = os.path.join(path, "video.mp4")
        download_video(video_url, video_local_path)
        text_to_speech_audio(caption, audio_path)
        output_file = combine_audio_video(audio_path, video_local_path, path)
        with open(output_file, "rb") as file:
            return file.read()


if __name__ == "__main__":
    AREAS = db.list_areas("0")[0]
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    for area in AREAS:
        os.makedirs(os.path.join(CURRENT_DIR, "videos"), exist_ok=True)
        os.makedirs(os.path.join(CURRENT_DIR, "videos/final"), exist_ok=True)
        print(f"Generating video for area {area['id']}")
        video_local_path = os.path.join(CURRENT_DIR, f"videos/video_{area['id']}.mp4")
        audio_path = os.path.join(CURRENT_DIR, f"videos/audio_{area['id']}.mp3")
        download_video(area["video"], video_local_path)
        description = generate_descriptions(area, video_local_path)
        text_to_speech_audio(description, audio_path)
        combine_audio_video(
            audio_path, video_local_path, os.path.join(CURRENT_DIR, "videos/final")
        )
