from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import file_audio_api 

app = FastAPI(
    title="Audio_transctipt_NXT",
    description="Audio Transcription",
    debug=True,
)

# Include the audio upload router
app.include_router(file_audio_api.router)

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
