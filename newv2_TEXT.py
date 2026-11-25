
import os
from pathlib import Path
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS


# ----------------------------------
# 1. LOAD API KEY
# ----------------------------------

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Groq API key not found in .env file.")

client = Groq(api_key=GROQ_API_KEY)


# ----------------------------------
# 2. SPEECH TO TEXT
# ----------------------------------

def speech_to_text(audio_bytes):

    transcription = client.audio.transcriptions.create(
        file=("recording.wav", audio_bytes),
        model="whisper-large-v3-turbo",
        language="en"
    )

    return transcription.text.strip()


# ----------------------------------
# 3. AI RESPONSE
# ----------------------------------

def get_ai_response(user_text):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI voice assistant. "
                    "Understand the user's question and provide "
                    "a clear, accurate and simple answer. "
                    "Keep responses concise and natural for speech."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ],

        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


# ----------------------------------
# 4. TEXT TO SPEECH
# ----------------------------------

def text_to_speech(text):

    tts = gTTS(
        text=text,
        lang="en"
    )

    audio_buffer = BytesIO()

    tts.write_to_fp(audio_buffer)

    return audio_buffer.getvalue()


# ----------------------------------
# 5. COMPLETE VOICE ASSISTANT
# ----------------------------------

def process_audio(audio_bytes):

    # Convert voice into text
    user_text = speech_to_text(audio_bytes)

    if not user_text:
        raise ValueError("No speech detected. Please record again.")

    # Generate AI answer
    ai_response = get_ai_response(user_text)

    # Convert AI answer into audio
    response_audio = text_to_speech(ai_response)

    return user_text, ai_response, response_audio
