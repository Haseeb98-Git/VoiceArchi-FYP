import React, {useState, useEffect, useRef} from "react";
import mic_icon from "../assets/mic_icon.svg";
import send_icon from "../assets/send_icon.svg";


const CreateFloorplan = () =>{
    const [isRecording, setIsRecording] = useState(false);
    const [recordTime, setRecordTime] = useState(0);
    const [audioBlob, setAudioBlob] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false); // Prevent early sending
    const mediaRecorderRef = useRef(null);
    const timerRef = useRef(null);
    const [messages, setMessages] = useState([]); // Single list for both user and system messages
    const [inputMessage, setInputMessage] = useState("");
    const messagesEndRef = useRef(null); // Reference for auto-scroll
    const [isMoved, setIsMoved] = useState(false);


    // Function to auto-scroll to the latest message
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
  
    // Scroll to bottom whenever messages change
    useEffect(() => {
      scrollToBottom();
    }, [messages]);


    const recordMessage = async () => {
      if (!isRecording) {
        // Start Recording
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
            setAudioBlob(audioBlob);
    
            // Send the message immediately after stopping
            const audioURL = URL.createObjectURL(audioBlob);
            setMessages((prev) => [...prev, { audio: audioURL, sender: "user" }]);
    
            // Create a download link and trigger download
            const downloadLink = document.createElement("a");
            downloadLink.href = audioURL;
            downloadLink.download = `recording_${Date.now()}.wav`;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
    
            // Simulate system response
            setTimeout(() => {
              setMessages((prev) => [...prev, { text: "Audio received!", sender: "system" }]);
            }, 1000);
          };
    
          mediaRecorder.start();
          setIsRecording(true);
          setRecordTime(0);
    
          // Start Timer
          timerRef.current = setInterval(() => {
            setRecordTime((prev) => prev + 1);
          }, 1000);
        } catch (error) {
          console.error("Error accessing microphone:", error);
        }
      } else {
        // Stop Recording and Send Message
        mediaRecorderRef.current?.stop();
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