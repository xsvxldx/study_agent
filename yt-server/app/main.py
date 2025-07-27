from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL
from pathlib import Path
import uuid

app = FastAPI()
AUDIO_DIR = Path("/app/downloads")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/download-audio/")
async def download_audio(youtube_url: str = Form(...)):
    audio_id = str(uuid.uuid4())
    output_path = AUDIO_DIR / f"{audio_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "audio_url": f"http://yt-dlp-server:8000/audio/{audio_id}.mp3"
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = AUDIO_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type='audio/mpeg', filename=filename)
