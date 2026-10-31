# --------------------------------------------------------
# Core Backend Service
# Domain: Engineering and Technology
# Focus: Applied Mathematics and Artificial Intelligence
# Field: Computer and Data Science
# Created by: MOHAMED HATEM MOHAMED ABDELAZIZ MOHAMED 
#           & EBRAHIM MOHAMED EBRAHIM HAMADA RASAD
# --------------------------------------------------------

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from gtts import gTTS
import os
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = "static"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

app.mount("/static", StaticFiles(directory=AUDIO_DIR), name="static")

# Initializing Google GenAI Client
client = genai.Client()

class Payload(BaseModel):
    text: str

def is_arabic(text: str) -> bool:
    # Pattern to verify if characters fall inside Arabic Unicode Range
    return bool(re.search(r'[\u0600-\u06FF]', text))

def generate_ai_summary(input_text: str, target_lang: str) -> str:
    if target_lang == "ar":
        prompt = f"قم بتلخيص المقال التالي بأسلوب واضح، مختصر، ومفهوم:\n\n{input_text}"
    else:
        prompt = f"Summarize the following article in a clear, concise, and professional manner:\n\n{input_text}"
        
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.strip()

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/team.html")
async def read_team():
    return FileResponse("team.html")

@app.post("/summarize")
async def handle_summary(data: Payload):
    if not data.text or not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        # Detect character structure to configure proper output localization
        lang_code = "ar" if is_arabic(data.text) else "en"
        
        # Request context summarization from live AI structural models
        result_text = generate_ai_summary(data.text, lang_code)
        
        # Audio rendering execution path using designated localization settings
        tts_engine = gTTS(text=result_text, lang=lang_code, slow=False)
        filename = "summary_audio.mp3"
        tts_engine.save(os.path.join(AUDIO_DIR, filename))
        
        return {
            "status": "success",
            "summary": result_text,
            "audio_url": f"/static/{filename}"
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
