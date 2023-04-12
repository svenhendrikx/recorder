import os
import datetime

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()


data_dir = "data"
Path(data_dir).mkdir(parents=True, exist_ok=True)

app = FastAPI()


@app.post("/recording")
async def save_recording(audio: UploadFile = File(...)):
    try:
        filename = f"audio_{datetime.datetime.now().strftime('%H:%M:%S_%d-%m-%Y')}"
        audio_file_path = os.path.join(data_dir, filename)
        
        # Save the audio file to disk
        with open(audio_file_path, "wb") as f:
            f.write(await audio.read())

        return JSONResponse(content={"message": "Recording saved successfully"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error saving recording"}, status_code=500)

# Place After All Other Routes
app.mount('', StaticFiles(directory="front/public/", html=True), name="static")
