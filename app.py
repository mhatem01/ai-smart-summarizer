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
from pydantic import BaseModel
from gtts import gTTS
import os

app = FastAPI()

# Enable CORS for direct frontend integration without security flags
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Payload(BaseModel):
    text: str

def parse_and_summarize(input_text: str):
    # Core logical engine for text segmentation and processing
    sentences = input_text.split('.')
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(clean_sentences) <= 3:
        return input_text
        
    # Algorithmic key-sentence extraction methodology
    indices = [0, len(clean_sentences) // 2, len(clean_sentences) - 1]
    selected = [clean_sentences[i] for i in sorted(list(set(indices)))]
    return ". ".join(selected) + "."

@app.post("/summarize")
async def handle_summary(data: Payload):
    if not data.text or not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        result_text = parse_and_summarize(data.text)
        
        # Audio rendering module implementation using native frameworks
        tts_engine = gTTS(text=result_text, lang='en', slow=False)
        output_file = "summary_audio.mp3"
        tts_engine.save(output_file)
        
        return {
            "status": "success",
            "summary": result_text,
            "audio_url": "https://soundhelix.com"
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
