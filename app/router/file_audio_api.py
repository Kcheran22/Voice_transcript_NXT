from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio_transcribe import upload_audio_to_s3

router = APIRouter(prefix="/audio", tags=["Audio Upload"])

@router.post("/upload")
async def upload_audio(name: str, file: UploadFile = File(...)):
    try:
        file_url = upload_audio_to_s3(name, file)
        return {
            "status": "success",
            "file_name": file.filename,
            "uploaded_as": name,
            "s3_url": file_url
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
