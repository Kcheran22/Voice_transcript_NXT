import boto3
import assemblyai as aai

# -------------------
# AssemblyAI API Key
# -------------------
aai.settings.api_key = "898d26f4173c45aa8600d238e67d5da6"

# -------------------
# Generate Presigned URL from S3
# -------------------
s3 = boto3.client("s3")

def generate_presigned_url(bucket, key, expiry=3600):
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiry
    )


# Your S3 audio file
bucket = "transcribe-audio-chatbot"
key = "upload/jee_20251212_065556.m4a"

# Generate temporary public URL
audio_url = generate_presigned_url(bucket, key)
print("Audio URL:", audio_url)

# -------------------
# Send to AssemblyAI
# -------------------
config = aai.TranscriptionConfig(speech_models=["universal"])

transcript = aai.Transcriber(config=config).transcribe(audio_url)

if transcript.status == "error":
    raise RuntimeError(f"Transcription failed: {transcript.error}")

print("TRANSCRIBED TEXT:")
print(transcript.text)
