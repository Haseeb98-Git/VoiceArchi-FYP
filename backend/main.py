from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
import requests
import json
from voicearchi_schemas import voiceArchi_json_schema, ambiguity_resolution_user_choice_schema
import utility_functions


openai_api_key = "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"
openrouter_api_key = "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"
openrouter_models = [("anthropic/claude-3.5-haiku","Anthropic"), ("mistralai/mistral-small-24b-instruct-2501","Mistral"), ("deepseek/deepseek-r1-distill-qwen-32b", "Fireworks"), ("google/gemini-2.0-flash-001", "Google AI Studio")]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=openai_api_key)


@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    message_count: int = Form(...)
):
    try:
        # Read the uploaded file into a buffer
        audio_bytes = await file.read()
        print(f"Received file size: {len(audio_bytes)} bytes")  # Debugging log
        print(f"File content type: {file.content_type}")
        print(f"User message count: {message_count}")  # Log message count
        
        audio_buffer = io.BytesIO(audio_bytes)
        audio_buffer.name = "recording.wav"

        # Transcribe using Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer  
        )

        if message_count == 0 or message_count == 2 or message_count == 3:
           return {"text": transcription.text}

        if message_count == 1:
            
            prompt = f"The user has been asked if they want to finalize the floorplan creation, or begin the ambiguity resolution (a feature in our app), your job is to extract user's answer in JSON. Here is the user's answer:\n\"{transcription.text}\"\n {ambiguity_resolution_user_choice_schema}"

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": openrouter_models[3][0],
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "provider": {
                        "order": [openrouter_models[3][1], openrouter_models[3][1]],
                        "allow_fallbacks": False
                    },
                }
            )

            print(f"Status Code: {response.status_code}")  # Debugging
            print(f"Response Text: {response.text}")  # Print the full response

            try:
                response_data = response.json()  # Attempt to parse JSON response
                if "choices" not in response_data:
                    raise HTTPException(status_code=500, detail="Invalid response format from OpenRouter")
                
                llm_response = response_data["choices"][0]["message"]["content"]

                def extract_json(text):
                    start = text.find("{")
                    end = text.rfind("}")
                    if start != -1 and end != -1 and start < end:
                        return text[start:end+1]  
                    return None

                extracted_json = extract_json(llm_response)
                if extracted_json:
                    return {"text": transcription.text, "user_choice_json": json.loads(extracted_json)}
                else:
                    raise HTTPException(status_code=400, detail="Could not extract JSON from response")
            
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Failed to parse JSON response from OpenRouter")
            
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
    
class FloorplanRequest(BaseModel):
    user_floorplan_description: str

@app.post("/extract_constraints")
async def extract_constraints(request: FloorplanRequest):
    prompt = f"For this text, extract constraints from it and give me result in JSON:\n\"{request.user_floorplan_description}\"\n {voiceArchi_json_schema}"

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": openrouter_models[3][0],
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "provider": {
                "order": [openrouter_models[3][1], openrouter_models[3][1]],
                "allow_fallbacks": False
            },
        }
    )

    print(f"Status Code: {response.status_code}")  # Debugging
    print(f"Response Text: {response.text}")  # Print the full response

    try:
        response_data = response.json()  # Attempt to parse JSON response
        if "choices" not in response_data:
            raise HTTPException(status_code=500, detail="Invalid response format from OpenRouter")
        
        llm_response = response_data["choices"][0]["message"]["content"]

        def extract_json(text):
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and start < end:
                return text[start:end+1]  
            return None

        extracted_json = extract_json(llm_response)
        general_ambiguities, size_ambiguities = utility_functions.get_ambiguities(json.loads(extracted_json))
        if extracted_json:
            return {"extracted_constraints": json.loads(extracted_json), "general_ambiguities": general_ambiguities, "size_ambiguities": size_ambiguities} 
        else:
            raise HTTPException(status_code=400, detail="Could not extract JSON from response")
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON response from OpenRouter")

    # Run using: uvicorn main:app --host 0.0.0.0 --port 8000 --reload