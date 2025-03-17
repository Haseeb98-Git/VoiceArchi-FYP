import React, {useState, useEffect, useRef} from "react";
import mic_icon from "../assets/mic_icon.svg";
import send_icon from "../assets/send_icon.svg";
import axios from "axios";

const CreateFloorplan = () =>{
    const [isRecording, setIsRecording] = useState(false);
    const [recordTime, setRecordTime] = useState(0);
    const [hasGeneratedSpeech, setHasGeneratedSpeech] = useState(false);
    const mediaRecorderRef = useRef(null);
    const timerRef = useRef(null);
    // messages is an array of objects, each object can have any number of properties that we can define dynamically, e.g. sender, text etc.
    // javascript objects don't have to follow a strict schema like typescript or languages like Java.
    const [messages, setMessages] = useState([]); // Single list for both user and system messages
    const [inputMessage, setInputMessage] = useState("");
    const messagesEndRef = useRef(null); // Reference for auto-scroll
    const [isMoved, setIsMoved] = useState(false);
    const hasRun = useRef(false);
    const userMessageCount = useRef(0); // ✅ Keeps value between re-renders
    const [userMessageTrigger, setUserMessageTrigger] = useState(false);

    

    // Function to auto-scroll to the latest message
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
      if (hasRun.current) return;
      hasRun.current = true;
    
      // Add initial "..." message
      setMessages((prev) => [
        ...prev,
        { text: "...", sender: "system" },
      ]);
    
      // Generate speech
      const welcomeText = "Welcome to VoiceArchi. Please describe your floorplan idea. You can share information like the size, number of rooms, adjacency requirements etc.";
      generateSpeech(welcomeText);
    }, []);

    useEffect(() => {
      // Only run this effect if hasGeneratedSpeech is true
      if (!hasGeneratedSpeech) return;
      setHasGeneratedSpeech(false);
      let welcomeText = "WWelcome to VoiceArchi. Please describe your floorplan idea. You can share information like the size, number of rooms, adjacency requirements etc.";
      if (userMessageCount.current == 1){
        welcomeText = "WWe have received your floorplan description. Please wait while the system extracts the necessary constraints for the floorplan creation.";
      }
      // Remove the "..." message
      setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
    
      let index = 0;
    
      // Function to type out the text character by character
      const typeText = () => {
        if (index < welcomeText.length) {
          setMessages((prev) => {
            const lastMessage = prev[prev.length - 1];
    
            // If the last message is from the system, append the next character
            if (lastMessage?.sender === "system") {
              return [
                ...prev.slice(0, -1), // Keep all messages except the last one
                {
                  ...lastMessage,
                  text: lastMessage.text + welcomeText.charAt(index),
                },
              ];
            } else {
              // If no system message exists, create a new one with the first character
              return [
                ...prev,
                { text: welcomeText.charAt(index), sender: "system" },
              ];
            }
          });
    
          index++;
          setTimeout(typeText, 50); // Adjust typing speed here (lower = faster)
        }
      };
    
      // Start the typing animation
      typeText();
    }, [hasGeneratedSpeech]); // Run this effect only when hasGeneratedSpeech changes
    const generateSpeech = async (speechText) => {
      const formData = new FormData();
      formData.append("text", speechText);
    
      try {
        const response = await fetch("http://localhost:8000/tts", {
          method: "POST",
          body: formData,
        });
    
        if (!response.ok) throw new Error("Failed to generate speech");
        
        const audioBlob = await response.blob();
        const audioObjectUrl = URL.createObjectURL(audioBlob);
    
        // ✅ Play the audio without UI controls
        const audio = new Audio(audioObjectUrl);
        // Add an event listener for when the audio starts playing
        audio.onplay = () => {
          setHasGeneratedSpeech(true); // Set state only after audio starts playing
        };
        audio.play();
      } catch (error) {
        console.error("Error:", error);
      }
    };
    // Scroll to bottom whenever messages change
    useEffect(() => {
      scrollToBottom();
    }, [messages]);

    useEffect(()=>{
        if (userMessageCount.current == 1){
          // Implement logic for handling user's given constraints
          setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
          generateSpeech("We have received your floorplan description. Please wait while the system extracts the necessary constraints for the floorplan creation.");
        }
    }, [userMessageTrigger]);
    const recordMessage = async () => {
      if (!isRecording) {
          try {
              const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
              const mediaRecorder = new MediaRecorder(stream);
              mediaRecorderRef.current = mediaRecorder;
              const audioChunks = [];
  
              mediaRecorder.ondataavailable = (event) => {
                  audioChunks.push(event.data);
              };
  
              mediaRecorder.onstop = async () => {
                  const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                  const audioFile = new File([audioBlob], "recording.wav", { type: "audio/wav" });
                
                  // Create a download link
                const a = document.createElement("a");
                a.href = URL.createObjectURL(audioBlob);
                a.download = "recording.wav";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(a.href); // Free up memory

                  const formData = new FormData();
                  formData.append("file", audioFile);
  
                  try {
                      const response = await axios.post("http://127.0.0.1:8000/transcribe", formData, {
                          headers: {
                              "Content-Type": "multipart/form-data",
                          },
                      });
  
                      if (response.data.text) {
                          setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                          setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                          userMessageCount.current += 1;
                          setUserMessageTrigger(true);
                      }
                  } catch (error) {
                      console.error("Error sending audio:", error);
                      setMessages((prev) => [...prev, { text: "Failed to transcribe audio.", sender: "system" }]);
                  }
              };
  
              mediaRecorder.start();
              setIsRecording(true);
              setRecordTime(0);
  
              timerRef.current = setInterval(() => {
                  setRecordTime((prev) => prev + 1);
              }, 1000);
          } catch (error) {
              console.error("Error accessing microphone:", error);
          }
      } else {
          mediaRecorderRef.current?.stop();
          setMessages((prev) => [...prev, { text: "...", sender: "user" }]);
          setIsRecording(false);
          setRecordTime(0);
          clearInterval(timerRef.current);
      }
  };
  
  
    const sendMessage = () => {
      if (isRecording) {
        recordMessage(); // Stop recording (it will automatically send)
        return;
      }
    
      // Handle text messages
      if (!inputMessage.trim()) return;
    
      setMessages((prev) => [...prev, { text: inputMessage, sender: "user" }]);
    
      // Simulate system response
      setTimeout(() => {
        setMessages((prev) => [...prev, { text: "Hello, how can I help you?", sender: "system" }]);
      }, 1000);
    
      setInputMessage("");
    };
  

    return (
    <>
            <button
                onClick={() => setIsMoved(!isMoved)}
                className="hidden absolute top-20 left-80 px-4 py-2 bg-white text-black rounded-md"
            >
                Move Chat Box
            </button>

                {/* Chat box*/}

            <div
                className={`w-140 h-160 rounded-xl absolute left-1/2 transform -translate-x-1/2 top-30 bg-voicearchi_purple_glow/10 border border-white/20 transition-transform duration-500 ease-in-out ${
                isMoved ? "translate-x-32" : ""
                }`}
            >
                {/*Chat title*/}
                <h1 className="absolute left-1/2 transform -translate-x-1/2 text-white">
                Chat
                </h1>

                
            {/* Chat Messages */}
            <div className="absolute top-12 left-0 w-full h-[500px] overflow-y-auto p-4 flex flex-col space-y-2">
                {messages.map((msg, index) => (
                <div 
                key={index} 
                className={`px-3 py-2 rounded-xl w-fit max-w-[70%] whitespace-pre-wrap break-words
                ${msg.sender === "user" ? "bg-blue-500/30 text-white ml-auto mr-3 text-left" : "bg-voicearchi_purple_glow/20 text-white ml-3 text-left"}`}
                >
                    {msg.text}
                </div>
                ))}
            {/* Invisible div to ensure auto-scroll works */}
                <div ref={messagesEndRef} />
            </div>

            {/* Chat Input */}
            <div className="absolute left-10 bottom-5 w-100 h-auto">
                <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message"
                className="w-full px-4 py-2 rounded-3xl border border-gray-300/30 focus:border-voicearchi_purple_bright focus:outline-none focus:ring-blue-500 text-gray-100 bg-transparent"
                />
                <img
                src = {send_icon}
                alt = "send icon" 
                onClick={sendMessage} 
                className="-mt-10 ml-auto -mr-13 w-9 h-9 rounded-full border-1 hover:border-voicearchi_purple_bright"
                />
                {isRecording && (
                <span className="absolute -top-9 -right-25 text-xs text-white bg-black/30 px-2 py-1 rounded-md">
                    {`${Math.floor(recordTime / 60)}:${(recordTime % 60).toString().padStart(2, "0")}`}
                </span>
                )}
                <img
                src = {mic_icon}
                alt = "mic icon" 
                onClick={recordMessage} 
                className={`-mt-9 ml-auto -mr-25 w-9 h-9 rounded-full border-1 hover:border-voicearchi_purple_bright transition-colors duration-300 ${
                            isRecording ? "bg-voicearchi_purple_glow_dim" : "bg-transparent"}`}
                />                     
            </div>

                
            </div>

      </>

    );


};

export default CreateFloorplan;