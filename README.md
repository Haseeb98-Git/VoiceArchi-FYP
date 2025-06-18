<h1 align="center">
  <img src="https://github.com/user-attachments/assets/173d27aa-1359-45a8-9438-977b2f11fd63" alt="voicearchi_logo" width="120"/>
  <br/>
  VoiceArchi - AI-Powered Voice-to-Floorplan Generator  
</h1>

A web application that leverages AI technology to transform a user's spoken ideas into detailed 2D architectural drawings, streamlining the floorplan creation process, making it intuitive and accessible for everyone, regardless of their technical skills.

## Key Features  

- **Voice-Driven Design** – Describe your floorplan naturally using voice commands.  
- **Real-Time AI Chatbot Interaction** – Conversational AI guides you through the design process.  
- **LLM-Powered Constraint Extraction** – AI interprets your description into structured design constraints.  
- **2D Floorplan Generation** – Uses the **Squarified Treemap Algorithm** for space-efficient layouts.  
- **Save & Manage Floorplans** – Store and revisit your designs anytime.  

## Tech Stack  

- **Frontend:** React.js, TailwindCSS  
- **Backend:** FastAPI (Python)  
- **AI & Algorithms:** Matplotlib (for visualization), Custom Squarified Treemap Logic  
- **Database & Auth:** Firebase

## Architecture

<h1 align="left">
  <img src="https://github.com/user-attachments/assets/7b7b1e63-f797-47d6-b4ec-91d7c55f85d9" alt="voicearchi_logo" width="600"/>
  <br/>
</h1>

## How It Works  

1. **Log In** → Navigate to **Create Floorplan** and click **"Create New Floorplan"**.  
2. **Voice Interaction** – The AI chatbot asks you to describe your floorplan idea via voice.  
3. **Constraint Extraction** – The system converts your description into structured JSON constraints.  
4. **Ambiguity Resolution** – If details are missing, the AI asks clarifying questions.  
5. **Finalize & Generate** – Once confirmed, the system generates a **2D floorplan** using:  
   - **Squarified Treemap Algorithm** (for room layouts)  
   - **Custom Logic** (for corridors, doors, etc.)  

## Algorithm Implementation  

We implemented the approach from:  
> **"Automatic Real-Time Generation of Floor Plans Based on Squarified Treemaps Algorithm"**  
> *International Journal of Computer Games Technology*  

Our Python-based solution ensures efficient and realistic space allocation.  

## Video Demo


https://github.com/user-attachments/assets/759d0a0b-6896-4886-b780-6cb8ae4847ef



## Project Structure  

```  
voice-archi/  
├── (root)            # Frontend (React + Tailwind)  
├── backend/          # Backend (FastAPI)  
├── backend/drawing_system.py              # Squarified Treemap & Floorplan Logic
├── backend/main.py              # FastAPI endpoints
└── README.md  
```  

## Getting Started  

### Prerequisites  
- Node.js (for React frontend)  
- Python 3.8+ (for FastAPI backend)  
- Firebase account (for auth & storage)  

### Installation  
1. **Clone the repo**  
   ```bash  
   git clone https://github.com/Haseeb98-Git/VoiceArchi-FYP  
   ```  

2. **Set up the backend**  
   ```bash  
   cd backend  
   pip install -r requirements.txt  
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload  
   ```  

3. **Set up the frontend**  
   ```bash    
   npm install
   npm run dev
   ```

4. **Set up API keys**
   - Navigate to the backend folder
   - Create a file called api_keys.py
   - Create variables openai_api_key and openrouter_api_key and set the values to your API keys

## License  
MIT  
