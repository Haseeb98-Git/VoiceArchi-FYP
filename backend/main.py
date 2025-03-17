from fastapi import FastAPI, File, UploadFile, Form
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Read the uploaded file into a buffer
        audio_bytes = await file.read()
        print(f"Received file size: {len(audio_bytes)} bytes")  # Debugging log
        print(f"File content type: {file.content_type}")
        audio_buffer = io.BytesIO(audio_bytes)
        
        # Assign a proper name to the buffer (required for OpenAI API)
        audio_buffer.name = "recording.wav"

        # Transcribe using Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer  # Pass the buffer instead of file.file
        )

        return {"text": transcription.text}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/tts")
async def generate_speech(text: str = Form(...)):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="ash",  # You can change to "echo", "fable", etc.
            input=text
        )

        # Stream the response directly
        return StreamingResponse(response.iter_bytes(), media_type="audio/mpeg")
    
    except Exception as e:
        return {"error": str(e)}