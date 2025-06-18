# VoiceArchi - AI-Powered Voice-to-Floorplan Generator  

<h1 align="center">
  <img src="https://github.com/user-attachments/assets/173d27aa-1359-45a8-9438-977b2f11fd63" alt="voicearchi_logo" width="200"/>
  <br/>
  VoiceArchi
</h1>

Transform your spoken ideas into detailed 2D architectural floorplans effortlessly with **VoiceArchi**, an AI-driven web application that makes architectural design intuitive and accessible to everyone—no technical skills required.  

## 🚀 Key Features  

- **🎙️ Voice-Driven Design** – Describe your floorplan naturally using voice commands.  
- **🤖 Real-Time AI Chatbot Interaction** – Conversational AI guides you through the design process.  
- **🧠 LLM-Powered Constraint Extraction** – AI interprets your description into structured design constraints.  
- **📐 2D Floorplan Generation** – Uses the **Squarified Treemap Algorithm** for space-efficient layouts.  
- **📂 Save & Manage Floorplans** – Store and revisit your designs anytime.  

## 🛠️ Tech Stack  

- **Frontend:** React.js, TailwindCSS  
- **Backend:** FastAPI (Python)  
- **AI & Algorithms:** Matplotlib (for visualization), Custom Squarified Treemap Logic  
- **Database & Auth:** Firebase  

## 📖 How It Works  

1. **Log In** → Navigate to **Create Floorplan** and click **"Create New Floorplan"**.  
2. **Voice Interaction** – The AI chatbot asks you to describe your floorplan idea via voice.  
3. **Constraint Extraction** – The system converts your description into structured JSON constraints.  
4. **Ambiguity Resolution** – If details are missing, the AI asks clarifying questions.  
5. **Finalize & Generate** – Once confirmed, the system generates a **2D floorplan** using:  
   - **Squarified Treemap Algorithm** (for room layouts)  
   - **Custom Logic** (for corridors, doors, etc.)  

## 🔍 Algorithm Implementation  

We implemented the approach from:  
> **"Automatic Real-Time Generation of Floor Plans Based on Squarified Treemaps Algorithm"**  
> *International Journal of Computer Games Technology*  

Our Python-based solution ensures efficient and realistic space allocation.  

## 📂 Project Structure  

```  
voice-archi/  
├── client/            # Frontend (React + Tailwind)  
├── server/            # Backend (FastAPI)  
├── algorithms/        # Squarified Treemap & Floorplan Logic  
├── firebase/          # Authentication & Database  
└── README.md  
```  

## 🚀 Getting Started  

### Prerequisites  
- Node.js (for React frontend)  
- Python 3.8+ (for FastAPI backend)  
- Firebase account (for auth & storage)  

### Installation  
1. **Clone the repo**  
   ```bash  
   git clone https://github.com/yourusername/voice-archi.git  
   ```  

2. **Set up the backend**  
   ```bash  
   cd server  
   pip install -r requirements.txt  
   uvicorn main:app --reload  
   ```  

3. **Set up the frontend**  
   ```bash  
   cd client  
   npm install  
   npm start  
   ```  

4. **Configure Firebase**  
   - Add your Firebase config in `client/src/firebase.js`.  

## 📜 License  
MIT  

## ✉️ Contact  
[Your Name] – [Your Email]  
Project Link: [https://github.com/yourusername/voice-archi](https://github.com/yourusername/voice-archi)  

---  

**VoiceArchi** makes architectural design as easy as speaking. Try it now! 🏡✨
