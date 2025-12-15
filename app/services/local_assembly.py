from fastapi import FastAPI
from pydantic import BaseModel
import assemblyai as aai
import json

# AssemblyAI Key
aai.settings.api_key = "898d26f4173c45aa8600d238e67d5da6"

# Local audio file path
LOCAL_AUDIO_FILE = "/Users/cherankathiresan/Documents/Voice_report/Voice_transcript_NXT/New recording 1.m4a"

app = FastAPI()

# Request body model
class FileInfo(BaseModel):
    file_name: str
    date: str

@app.post("/file-info")
def get_file_info(info: FileInfo):
    """
    API that:
    1. Accepts file_name and date
    2. Transcribes local audio file
    3. Returns everything as JSON
    """

    # Transcribe the local audio file
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(LOCAL_AUDIO_FILE)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    # Prepare final JSON output
    json_payload = {
        "name": info.file_name,
        "date": info.date,
        "transcript": transcript.text
    }

    return json_payload
