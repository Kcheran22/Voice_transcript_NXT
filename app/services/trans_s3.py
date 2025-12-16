import boto3
import time
import urllib.request
import json

# --- Configuration ---
# Set your region (e.g., 'us-west-2') and S3 URI (e.g., 's3://your-bucket-name/your-audio-file.mp3')
AWS_REGION = 'us-west-2'
JOB_URI = 's3://transcript-audio-chatbot/uploads/jee_20251212_065556.mp3'
MEDIA_FORMAT = JOB_URI.split('.')[-1]
JOB_NAME = 'jee_20251212_065556'
LANGUAGE_CODE = 'en-US'

# ---------------------

transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)

def start_transcription_job(job_name, job_uri, media_format, language_code):
    """Starts an asynchronous transcription job."""
    print(f"Starting transcription job: {job_name}...")
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=media_format,
        LanguageCode=language_code
    )

def check_job_status(job_name):
    """Polls AWS for job completion status."""
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job status: {job_status}")
            return status
        print("Not ready yet, waiting 5 seconds...")
        time.sleep(5) # Wait before polling again

def get_transcription_result(status):
    """Retrieves the final transcript text from the result URI."""
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"Downloading transcript from: {transcript_uri}")
        
        # Download and parse the JSON content
        with urllib.request.urlopen(transcript_uri) as response:
            result_json = json.loads(response.read().decode("utf-8"))
            transcript_text = result_json['results']['transcripts'][0]['transcript']
            print("\n--- Transcription Text ---")
            print(transcript_text)
            print("--------------------------")
            return transcript_text
    else:
        print("Transcription job failed.")
        return None

# --- Main execution ---
if __name__ == "__main__":
    start_transcription_job(JOB_NAME, JOB_URI, MEDIA_FORMAT, LANGUAGE_CODE)
    job_status_response = check_job_status(JOB_NAME)
    get_transcription_result(job_status_response)

