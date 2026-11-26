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
import re
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

app.mount("/static", StaticFiles(directory=AUDIO_DIR), name="static")

class Payload(BaseModel):
    text: str

def is_arabic(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))

def get_groq_keys() -> list:
    raw_keys = os.environ.get("GROQ_API_KEYS") or os.environ.get("GROQ_API_KEY") or ""
    keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
    for i in range(1, 10):
        extra = os.environ.get(f"GROQ_API_KEY_{i}", "").strip()
        if extra and extra not in keys:
            keys.append(extra)
    return keys

def generate_external_ai_summary(input_text: str, target_lang: str) -> str:
    api_keys = get_groq_keys()
    if not api_keys:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is missing.")

    api_url = "https://groq.com"

    if target_lang == "ar":
        system_prompt = "Summarize the following text clearly and concisely in Arabic without any introductory or conversational text:"
    else:
        system_prompt = "Summarize the following text clearly and concisely in English without any introductory or conversational text:"

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    last_error = "Unknown error"

    for api_key in api_keys:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=20)
            if response.status_code == 200:
                result_data = response.json()
                return result_data["choices"][0]["message"]["content"].strip()
            else:
                last_error = f"Status {response.status_code}: {response.text}"
        except Exception as e:
            last_error = str(e)
            continue

    raise HTTPException(status_code=502, detail=f"All Groq API keys failed. Last error: {last_error}")

@app.get("/")
async def read_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found on server.")
    return FileResponse(index_path)

@app.get("/team.html")
async def read_team():
    team_path = os.path.join(BASE_DIR, "team.html")
    if not os.path.exists(team_path):
        raise HTTPException(status_code=404, detail="team.html not found on server.")
    return FileResponse(team_path)

@app.post("/summarize")
async def handle_summary(data: Payload):
    if not data.text or not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        lang_code = "ar" if is_arabic(data.text) else "en"
        result_text = generate_external_ai_summary(data.text, lang_code)

        tts_engine = gTTS(text=result_text, lang=lang_code, slow=False)
        filename = "summary_audio.mp3"
        tts_engine.save(os.path.join(AUDIO_DIR, filename))

        return {
            "status": "success",
            "summary": result_text,
            "audio_url": f"/static/{filename}"
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
