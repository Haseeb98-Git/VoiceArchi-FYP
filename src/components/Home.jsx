import React, {useState, useEffect, useRef} from "react";
import Intro from "../components/Intro";
import background_pattern from "../assets/background_pattern_1.svg";
import mic_icon from "../assets/mic_icon.svg";
import send_icon from "../assets/send_icon.svg";


const Home = () =>{
    const [messages, setMessages] = useState([]); // Single list for both user and system messages
    const [inputMessage, setInputMessage] = useState("");
    const messagesEndRef = useRef(null); // Reference for auto-scroll

    // Function to auto-scroll to the latest message
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
  
    // Scroll to bottom whenever messages change
    useEffect(() => {
      scrollToBottom();
    }, [messages]);

    const sendMessage = () => {
      if (!inputMessage.trim()) return; // Prevent empty messages
  
      // Append user message
      setMessages((prev) => [...prev, { text: inputMessage, sender: "user" }]);
  
      // Simulate system response after 1 second
      setTimeout(() => {
        setMessages((prev) => [...prev, { text: "Hello, how can I help you?", sender: "system" }]);
      }, 1000);
  
      setInputMessage(""); // Clear input after sending
    };

    let loggedIn = false;
    const [isMoved, setIsMoved] = useState(false);
    return (
        <>

    {loggedIn?

    <>
    {/* Content when the user is not logged in. */}

    {/* Main Background */}
      <div className="brightness-150 relative w-full max-w-full overflow-hidden bg-voicearchi_dark_background text-white">

        {/* Glowing Effects (Do Not Remove) */}
        <div className="absolute left-1/2 transform -translate-x-1/2 -top-60 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
        <div className="absolute left-1/2 transform -translate-x-1/2 bottom-500 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
        <img src={background_pattern} alt="Background pattern SVG" className="w-140 h-auto opacity-8 absolute left-17 top-10" />
        <img src={background_pattern} alt="Background pattern SVG" className="w-140 h-auto scale-x-[-1] opacity-8 absolute -right-10 top-60" />
        {/* Page Containers */}

        {/* Intro Page Content */}
        <Intro/>

        <div className="relative h-screen w-full flex items-center justify-center">
          <h1 className="text-4xl font-bold">About VoiceArchi</h1>
        </div>
        <div className="relative h-screen w-full flex items-center justify-center">
          <h1 className="text-4xl font-bold">Features</h1>
        </div>
        <div className="relative h-screen w-full flex items-center justify-center">
          <h1 className="text-4xl font-bold">Showcase</h1>
        </div>
        <div className="relative h-screen w-full flex items-center justify-center">
          <h1 className="text-4xl font-bold">Contact Us</h1>
        </div>
      </div>
      </>
      : 
      <>
            <div className="brightness-150 relative w-full h-screen max-w-full overflow-hidden bg-voicearchi_dark_background text-white">
            {/* Glowing Effects (Do Not Remove) */}
            <div className="absolute left-1/2 transform -translate-x-1/2 -top-60 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
            <img src={background_pattern} alt="Background pattern SVG" className="w-140 h-auto opacity-8 absolute left-17 top-10" />
            <img src={background_pattern} alt="Background pattern SVG" className="w-140 h-auto scale-x-[-1] opacity-8 absolute -right-10 top-60" />
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
                  <img
                    src = {mic_icon}
                    alt = "mic icon" 
                    onClick={sendMessage} 
                    className="-mt-9 ml-auto -mr-25 w-9 h-9 rounded-full border-1 hover:border-voicearchi_purple_bright"
                  />                     
                </div>

                  
                </div>
            </div>

      </>
      }
        </>

    );


};

export default Home;