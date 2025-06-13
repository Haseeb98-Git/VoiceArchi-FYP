from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import io
import requests
import json
from voicearchi_schemas import voiceArchi_json_schema, ambiguity_resolution_user_choice_schema
import utility_functions
import drawing_system as ds
from drawing_system import area_types, room_sizes
from typing import Dict, Any
import copy
import api_keys

openai_api_key = api_keys.openai_api_key
openrouter_api_key = api_keys.openrouter_api_key
openrouter_api_key_2 = api_keys.openrouter_api_key_2

openrouter_models = [("anthropic/claude-3.5-haiku","Anthropic"), ("mistralai/mistral-small-24b-instruct-2501","Mistral"),
                     
                      ("deepseek/deepseek-r1-distill-qwen-32b", "Fireworks"), ("google/gemini-2.0-flash-001", "Google AI Studio"),

                      ("deepseek/deepseek-r1-zero:free", "Chutes"), ("anthropic/claude-3.7-sonnet", "Anthropic"),

                      ("qwen/qwen2.5-vl-72b-instruct:free", "Alibaba"), ("qwen/qwen2.5-vl-72b-instruct", "Parasail"),
                      ("deepseek/deepseek-chat-v3-0324", "Parasail")]

active_openrouter_api_key = openrouter_api_key
active_openrouter_model = openrouter_models[8][0]
active_openrouter_modeL_provider = openrouter_models[8][1]

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
                    "Authorization": f"Bearer {active_openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": active_openrouter_model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "provider": {
                        "order": [active_openrouter_modeL_provider, active_openrouter_modeL_provider],
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
                    print("Returning response:", {"text": transcription.text, "user_choice_json": json.loads(extracted_json)})
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
            "Authorization": f"Bearer {openrouter_api_key_2}",
            "Content-Type": "application/json"
        },
        json={
            "model": active_openrouter_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "provider": {
                "order": [active_openrouter_modeL_provider, active_openrouter_modeL_provider],
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

class ConstraintsRequest(BaseModel):
    user_constraints: dict
@app.post("/drawing")
def drawing(data: ConstraintsRequest):
    
    user_constraints = data.user_constraints
    print("🔹 Received JSON:")
    print(json.dumps(user_constraints, indent=4))  # Pretty-print the JSON
    # Here, process the extracted constraints and generate the floorplan image
    user_constraints = data.user_constraints

    # Run the processing pipeline
    constraints, room_name_mappings = ds.get_constraints_room_mappings(user_constraints, room_sizes)
    grouped_rooms = ds.group_rooms(constraints, area_types)
    squarified_areas = ds.squarify_areas(grouped_rooms)
    room_data, graph = ds.get_room_data_and_graph(grouped_rooms, squarified_areas)
    label_positions = ds.get_room_label_positions(room_data)

    room_data_backbone = copy.deepcopy(room_data)
    room_data_backbone = ds.convert_to_absolute(room_data_backbone)
    graph_data = ds.convert_to_graph_with_room_info(room_data_backbone)
    updated_graph_data = ds.remove_outside_edges_and_corners(graph_data)
    new_graph, connecting_vertices = ds.remove_room(updated_graph_data, "livingroom_1")

    disconnected_rooms = ds.get_disconnected_rooms(room_data)
    shortest_path_graph = ds.shortest_path_to_connect_rooms(new_graph, connecting_vertices[0][0], disconnected_rooms)
    cleaned_path = ds.remove_redundant_edges(shortest_path_graph)
    ds.plot_graph_with_path(graph_data, cleaned_path, corridor_width=45, padding=0)
    boundary_edges = ds.get_color_boundary_edges(image_path="corridor.png")
    normalized_edges = ds.resize_graph_edges(original_graph_edges=boundary_edges, original_size=2400, new_size=100)
    merged_normalized_edges = ds.merge_close_values_in_graph(normalized_edges)
    
    corridor_edges_dict = ds.format_corridor_edges(merged_normalized_edges)
    merged_edges = {**graph_data['edges'], **corridor_edges_dict}
    split_edges_new = ds.split_edges_at_intersections(merged_edges)
    unique_edges = ds.remove_duplicate_edges(split_edges_new)
    room_edges_in_corridor, corridor_polygon = ds.get_room_edges_within_corridor(merged_normalized_edges, unique_edges)

    corridor_edges, room_edges = ds.get_room_and_corridor_edges(unique_edges)
    corridor_edges_in_rooms = ds.get_corridor_edges_within_rooms(room_edges, corridor_edges)

    updated_edges = ds.remove_given_edges(unique_edges, room_edges_in_corridor)
    updated_edges_removed_corridor_from_living_room = ds.remove_corridor_edges_from_living_room(updated_edges, corridor_edges_in_rooms)
    room_edges_with_corridor_connection = ds.get_room_edges_with_corridor_connection(corridor_edges_in_rooms, updated_edges_removed_corridor_from_living_room)

    door_edges = ds.generate_door_edges(room_edges_with_corridor_connection)

    # Generate and save the final floorplan image
    save_path = "final_floorplan.png"
    ds.plot_graph_edges_with_doors(room_edges_with_corridor_connection, door_edges, label_positions, text_size=12, padding=5, save_path=save_path)

    return FileResponse(save_path, media_type="image/png", filename="floorplan.png")

    # Run using: uvicorn main:app --host 0.0.0.0 --port 8000 --reload