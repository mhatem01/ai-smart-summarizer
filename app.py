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
from gtts import gTTS
import os

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

class Payload(BaseModel):
    text: str

def parse_and_summarize(input_text: str):
    sentences = input_text.split('.')
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    if len(clean_sentences) <= 3:
        return input_text
    indices = [0, len(clean_sentences) // 2, len(clean_sentences) - 1]
    selected = [clean_sentences[i] for i in sorted(list(set(indices)))]
    return ". ".join(selected) + "."

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.post("/summarize")
async def handle_summary(data: Payload):
    if not data.text or not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        result_text = parse_and_summarize(data.text)
        tts_engine = gTTS(text=result_text, lang='en', slow=False)
        filename = "summary_audio.mp3"
        tts_engine.save(os.path.join(AUDIO_DIR, filename))
        
        return {
            "status": "success",
            "summary": result_text,
            "audio_url": f"/static/{filename}"
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
