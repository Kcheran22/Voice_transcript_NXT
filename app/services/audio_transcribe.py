import boto3
import datetime
from fastapi import UploadFile
from config import AWS_REGION, S3_BUCKET

def upload_audio_to_s3(name: str, file: UploadFile):
    """
    Uploads an audio/video file (mp3, m4a, mp4) to S3.
    """

    allowed_types = ["audio/mpeg", "audio/mp4", "audio/x-m4a", "video/mp4,audio/mp3"]

    if file.content_type not in allowed_types:
        raise ValueError("Invalid file type. Only mp3, m4a, mp4 are allowed.")

    s3 = boto3.client("s3", region_name=AWS_REGION)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    extension = file.filename.split(".")[-1]
    s3_key = f"uploads/{name}_{timestamp}.{extension}"

    file_data = file.file.read()

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=file_data,
        ContentType=file.content_type
    )

    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

