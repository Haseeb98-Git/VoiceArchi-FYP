import React, {useState, useEffect, useRef} from "react";
import mic_icon from "../assets/mic_icon.svg";
import send_icon from "../assets/send_icon.svg";
import axios from "axios";
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import JsonViewer from "./JsonViewer";

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
    const [constraintsWindowActive, setConstraintsWindowActive] = useState(false);
    const userMessageCount = useRef(0); // ✅ Keeps value between re-renders
    const [userMessageTrigger, setUserMessageTrigger] = useState(false);
    //const [userConstraints, setUserConstraints] = useState("");
    const userConstraints = useRef("");
    const [extractedData, setExtractedData] = useState(null);
    const [error, setError] = useState(null);
    const [isLoadingConstraints, setIsLoadingConstraints] = useState(false);
    const [isSystemTyping, setIsSystemTyping] = useState(false);
    const systemMessageCount = useRef(0);
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [generalAmbiguities, setGeneralAmbiguities] = useState(null);
    const [sizeAmbiguities, setSizeAmbiguities] = useState(null);
    const userChoiceAR = useRef("");
    const userResponseForGeneralAmbiguities = useRef("");
    const userResponseForSizeAmbiguities = useRef("");
    const [activeTab, setActiveTab] = useState("constraints"); // "constraints" or "floorplan"
    const [isFinalizedFloorplan, setIsFinalizedFloorplan] = useState(false);
    const [floorplanImage, setFloorplanImage] = useState(null); // Store image URL
    const [isLoadingFinalization, setIsLoadingFinalization] = useState(false);

    const waitForCondition = (conditionFn, interval = 100) => {
      return new Promise((resolve) => {
        const checkCondition = () => {
          if (conditionFn()) {
            resolve(); // ✅ Condition met, resolve the promise
          } else {
            setTimeout(checkCondition, interval); // ⏳ Retry after delay
          }
        };
        checkCondition();
      });
    };
    
    const handleFinalizeFloorplan = async () => {
      setIsLoadingFinalization(true);
  
      try {
          console.log("Finalizing Floorplan with:", extractedData); // Debugging
  
          const response = await axios.post(
              "http://localhost:8000/drawing",
              { user_constraints: extractedData },  // ✅ FIXED: Changed key name
              {
                  headers: {
                      "Content-Type": "application/json",
                  },
                  responseType: "blob",
              }
          );
  
          const imageURL = URL.createObjectURL(response.data);
          setFloorplanImage(imageURL);
          setIsFinalizedFloorplan(true);
      } catch (error) {
          console.error("Error finalizing floorplan:", error.response ? error.response.data : error);
      }
  
      setIsLoadingFinalization(false);
  };
  
  

    // Function to auto-scroll to the latest message
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
      if (!isChatStarted) return;
      // Add initial "..." message
      setMessages((prev) => [
        ...prev,
        { text: "...", sender: "system" },
      ]);
    
      // Generate speech
      const welcomeText = "Welcome to VoiceArchi. Please describe your floorplan idea. You can share information like the size, number of rooms, adjacency requirements etc.";
      generateSpeech(welcomeText);
    }, [isChatStarted]);

    useEffect(() => {
    
      // Only run this effect if hasGeneratedSpeech is true
      if (!hasGeneratedSpeech) return;
      setHasGeneratedSpeech(false);
    
      let systemMessageText = "WWelcome to VoiceArchi. Please describe your floorplan idea. You can share information like the size, number of rooms, adjacency requirements etc.";
      if (userMessageCount.current == 1) {
        systemMessageText = "WWe have received your floorplan description. Please wait while the system extracts the necessary constraints for the floorplan creation.";
      }
      if (userMessageCount.current == 1 && systemMessageCount.current == 3 && !isLoadingConstraints) {
        if (userChoiceAR.current == ""){
        systemMessageText = "YYour constraints have successfully been extracted. Would you like to resolve any ambiguities? Or you can choose to finalize the floorplan.";
        }
        else{
          systemMessageText = "WWould you like to see if there are more ambiguities? Or you can choose to finalize the floorplan.";
          userChoiceAR.current = "";
        }
      }
      if (userMessageCount.current == 2 && systemMessageCount.current == 4 && !isLoadingConstraints){
          if (userChoiceAR.current == "resolve_ambiguities"){
            if (Object.values(generalAmbiguities).length > 0){
              let ambiguities_string = Object.values(generalAmbiguities).join("\n");
              systemMessageText = "SSure, lets resolve the following ambiguities: \n" + ambiguities_string;
            }
          }
      }
      if (userMessageCount.current == 3 && systemMessageCount.current == 5 && !isLoadingConstraints){
        if (userChoiceAR.current == "resolve_ambiguities"){
            if (Object.values(sizeAmbiguities).length > 0){
              let ambiguities_string = Object.values(sizeAmbiguities).join("\n");
              systemMessageText = "GGot it, now lets resolve the following ambiguities: \n" + ambiguities_string;
            }
            else{
              systemMessageText = "YYou have no more ambiguities left. You can finalize your floorplan.";
            }
        }
      }
      
      if (userMessageCount.current == 4 && systemMessageCount.current == 6){
        if (Object.values(generalAmbiguities).length > 0 || Object.values(sizeAmbiguities).length > 0){
           systemMessageText = "PPlease wait while we update your constraints based upon the given information.";
        }
        else{
          systemMessageText = "YYou have no more ambiguities. You can now finalize your floorplan.";
        }
      }

      if (userMessageCount.current == 4 && systemMessageCount.current == 7){
        if (Object.values(generalAmbiguities).length > 0 || Object.values(sizeAmbiguities).length > 0){
          systemMessageText = "PPlease wait while we update your constraints based upon the given information.";
       }
       else{
         systemMessageText = "YYou have no more ambiguities. You can now finalize your floorplan.";
       }
      }
    

    
      let index = 0;
    
      // Function to type out the text character by character
      const typeText = () => {
        setIsSystemTyping(true);
        if (index < systemMessageText.length) {
          setMessages((prev) => {
            const lastMessage = prev[prev.length - 1];
            // Remove the "..." message
            setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
            // If the last message is from the system, append the next character
          // 🛠️ Fix: Create a new message if the last one is "..." or not from system
          if (lastMessage?.sender === "system" && lastMessage.text !== "...") {
            return [
              ...prev.slice(0, -1),
              { ...lastMessage, text: lastMessage.text + systemMessageText.charAt(index) },
            ];
          } else {
            return [...prev, { text: systemMessageText.charAt(index), sender: "system" }];
          }
          });
    
          index++;
          setTimeout(typeText, 50); // Adjust typing speed here (lower = faster)
        } else {
          // ✅ Only set isSystemTyping to false AFTER the last character is typed
          setIsSystemTyping(false);
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
          systemMessageCount.current += 1;
          setHasGeneratedSpeech(true); // Set state only after audio starts playing
          if (userMessageCount.current == 1 && systemMessageCount.current == 2){
            setIsMoved(true);
            setConstraintsWindowActive(true);
            setIsLoadingConstraints(true);
            extractConstraints();
          }
          if (userMessageCount.current == 4 && userChoiceAR.current == "resolve_ambiguities"){
            if (Object.values(generalAmbiguities).length != 0 || Object.values(sizeAmbiguities).length != 0){
                setIsLoadingConstraints(true);
                setExtractedData(null);
                extractConstraints();
            }
          }
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

    const extractConstraints = async () => {
      try {
          const response = await axios.post("http://127.0.0.1:8000/extract_constraints", {
              user_floorplan_description: userConstraints.current
          });

          setExtractedData(response.data.extracted_constraints);
          setGeneralAmbiguities(response.data.general_ambiguities);
          setSizeAmbiguities(response.data.size_ambiguities);
          setError(null);
          setIsLoadingConstraints(false);
          console.log("usermessagecount: " + userMessageCount.current + " systemmessagecount: " + systemMessageCount.current);
          console.log("sent the following user message: "+ userConstraints.current);
          if (userChoiceAR.current == "resolve_ambiguities"){
            if (Object.values(generalAmbiguities).length != 0 || Object.values(sizeAmbiguities).length != 0){
                userMessageCount.current = 1;
                systemMessageCount.current = 2;
            }
          }
        
      } catch (err) {
          console.error("Error:", err);
          setError("Failed to extract constraints.");
      }
  };

  useEffect(() => {
    if (!isLoadingConstraints && userMessageCount.current == 1 && systemMessageCount.current == 2) {
      (async () => {
        await waitForCondition(() => !isSystemTyping); // ⏳ Wait until `isSystemTyping` is false
  
        // ✅ Now that `isSystemTyping` is false, proceed
        setMessages((prev) => [
          ...prev,
          { text: "...", sender: "system" },
        ]);
        if(userChoiceAR.current == ""){
          generateSpeech(
            "Your constraints have successfully been extracted. Would you like to resolve any ambiguities? Or you can choose to finalize the floorplan."
          );
        }
        else{
          generateSpeech(
            "Would you like to see if there are more ambiguities? Or you can choose to finalize the floorplan."
          );
        }
      })();
    }
    if (!isLoadingConstraints && userMessageCount.current == 4 && systemMessageCount.current == 6) {
      (async () => {
        await waitForCondition(() => !isSystemTyping); // ⏳ Wait until `isSystemTyping` is false
  
        // ✅ Now that `isSystemTyping` is false, proceed
        setMessages((prev) => [
          ...prev,
          { text: "...", sender: "system" },
        ]);
        console.log("yes executing");
        if (Object.values(sizeAmbiguities) != 0 || Object.values(generalAmbiguities) != 0){
            userMessageCount.current = 1;
            systemMessageCount.current = 2;
            generateSpeech("Would you like to see if there are more ambiguities? Or you can choose to finalize the floorplan.");
        } 
        else{
          generateSpeech(
            "You have no more ambiguities. You can finalize your floorplan."
          );
      }
      })();
    }
  }, [isLoadingConstraints, isSystemTyping]); // 🔥 Added `isSystemTyping` to dependencies
  

    useEffect(()=>{
        if (!userMessageTrigger) return;
        if (userMessageCount.current == 1){
          // Implement logic for handling user's given constraints
          setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
          generateSpeech("We have received your floorplan description. Please wait while the system extracts the necessary constraints for the floorplan creation.");
          setUserMessageTrigger(false);
        }
        if (userMessageCount.current == 2){
          if (userChoiceAR.current == "resolve_ambiguities"){
              if (Object.values(generalAmbiguities).length > 0){
                let ambiguities_string = Object.values(generalAmbiguities).join("\n");
                console.log(generalAmbiguities);
                setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
                generateSpeech("Sure, lets resolve the following ambiguities: \n" + ambiguities_string);
                setUserMessageTrigger(false);
              }
              else
              {
                userMessageCount.current = 3;
                systemMessageCount.current = 4;
              }

          }
        }

          //this executes when we have found general ambiguities.
        if (userMessageCount.current == 3){
          if (userChoiceAR.current == "resolve_ambiguities"){
              if (Object.values(sizeAmbiguities).length > 0){
                let ambiguities_string = Object.values(sizeAmbiguities).join("\n");
                setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
                generateSpeech("Got it, now lets resolve the following ambiguities: \n" + ambiguities_string);
                setUserMessageTrigger(false);
              }
              else{
                userMessageCount.current = 4;
                systemMessageCount.current = 6;
                if (Object.values(generalAmbiguities).length > 0){
                  let additional_string = "\n(Some questions were asked to the user about the floorplan):\n Questions: " + Object.values(generalAmbiguities).join("\n")
                                          + "\nAnswers: " + userResponseForGeneralAmbiguities.current + '\n';
                  console.log("sent: " + userConstraints.current + additional_string);
                  userConstraints.current = userConstraints.current + additional_string;
                }
              }

          }
        }
        if (userMessageCount.current == 4){
          if (userChoiceAR.current == "resolve_ambiguities"){
            // Implement logic for handling user's given constraints
            if (Object.values(generalAmbiguities).length > 0 || Object.values(sizeAmbiguities).length > 0){
                setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
                generateSpeech("Please wait while we update your constraints based upon the given information.");
                setUserMessageTrigger(false);
            }
            else{
                setMessages((prev) => [...prev, { text: "...", sender: "system" }]);
                generateSpeech("You have no more ambiguities. You can now finalize your floorplan.");
                setUserMessageTrigger(false);
            }
          }
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
                
                  const formData = new FormData();
                  formData.append("file", audioFile);
                  formData.append("message_count", userMessageCount.current); // Append user message count
                  try {
                      const response = await axios.post("http://127.0.0.1:8000/transcribe", formData, {
                          headers: {
                              "Content-Type": "multipart/form-data",
                          },
                      });
  
                      if (response.data.text && userMessageCount.current == 0) {
                          setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                          setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                          userConstraints.current = response.data.text;
                          userMessageCount.current += 1;
                          setUserMessageTrigger(true);
                      }
                      if (response.data.text && (userMessageCount.current == 2 || userMessageCount.current == 3)) {
                        setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                        setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                        userResponseForGeneralAmbiguities.current += response.data.text;

                        if (userMessageCount.current == 3){
                          userResponseForSizeAmbiguities.current += response.data.text;

                          let additional_string = "\n(Some questions were asked to the user about the floorplan):\n Questions: " + Object.values(generalAmbiguities).join("\n")
                                                   + "\nAnswers: " + userResponseForGeneralAmbiguities.current + "\n Questions: " + Object.values(sizeAmbiguities).join("\n")
                                                   + "\nAnswers: " + userResponseForSizeAmbiguities.current; 
                          userConstraints.current = userConstraints.current + additional_string;
                          console.log(userConstraints.current + additional_string);
                        }
                        userMessageCount.current += 1;
                        setUserMessageTrigger(true);
                      }
                      if (response.data.text && userMessageCount.current == 1) {
                        console.log("received response:" + response.data.text);
                          if (response.data.user_choice_json){
                            if (response.data.user_choice_json.user_choice == "resolve_ambiguities"){
                                setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                                console.log("Received response: " + response.data.text);
                                setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                                userMessageCount.current += 1;
                                setUserMessageTrigger(true);
                                userChoiceAR.current = response.data.user_choice_json.user_choice;
                                console.log("The user asked to resolve ambiguities.")
                                console.log(response.data.user_choice_json);
                            }
                            else if (response.data.user_choice_json.user_choice == "finalize_floorplan"){
                              setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                              setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                              userMessageCount.current += 1;
                              setUserMessageTrigger(true);
                              userChoiceAR.current = response.data.user_choice_json.user_choice;
                              console.log("The user asked to finalize the floorplan.")
                              console.log(response.data.user_choice_json);
                            }
                            else if (response.data.user_choice_json.user_choice == "the_user_did_not_answer"){
                              setMessages((prev) => prev.filter((msg) => msg.text !== "..."));
                              setMessages((prev) => [...prev, { text: response.data.text, sender: "user" }]);
                              // the userMessageCount remains the same because the user did not answer the question.
                              //userMessageCount.current += 1;
                              setUserMessageTrigger(true);
                              userChoiceAR.current = response.data.user_choice_json.user_choice;
                              console.log("The user did not answer the question.")
                              console.log(response.data.user_choice_json);
                            }
                          }
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
    
    
      setInputMessage("");
    };
  

    return (
    <>
                {/* Chat box*/}
            <button className={`rounded-full absolute left-1/2 transform -translate-x-1/2 top-1/2 -translate-y-1/2 text-2xl font-montserrat font-bold border-1 border-voicearchi_purple_bright py-2 px-8 z-50 hover:bg-voicearchi_purple_glow/60 ${isChatStarted? "hidden": ""}`}
                    onClick={()=>{setIsChatStarted(true);}}>
                Create New Floorplan
            </button>
            <div
                className={`w-140 h-160 rounded-xl absolute left-1/2 transform -translate-x-1/2 top-30 bg-voicearchi_purple_glow/10 border border-white/20 transition-transform duration-2000 ease-in-out ${
                isMoved ? "translate-x-35" : ""
                } ${isChatStarted ? "": "opacity-40 pointer-events-none"}`}
            >
                {/*Chat title*/}
                <h1 className="absolute left-1/2 transform -translate-x-1/2 text-white">
                Chat
                </h1>
                
            {/* Chat Messages */}
            <div className="absolute top-12 left-0 w-full h-[500px]  p-4 flex flex-col space-y-2 scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar scrollbar-thumb-voicearchi_purple_glow_dim/15 scrollbar-track-white/0 scrollbar-hover:scrollbar-thumb-voicearchi_purple_glow_dim/30 overflow-y-scroll">
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
                className={`-mt-10 ml-auto -mr-13 w-9 h-9 rounded-full border-1 hover:border-voicearchi_purple_bright ${isSystemTyping ? "opacity-40 pointer-events-none" : ""}`}
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
                            isRecording ? "bg-voicearchi_purple_glow_dim" : "bg-transparent"} ${
                            isSystemTyping ? "opacity-40 pointer-events-none" : ""}`}
                />                     
            </div>

                
            </div>


            {/*Constraints and floorplan drawing window*/}
            <div
            className={`w-140 h-160 rounded-xl absolute left-85 top-30 animate-fade-delayed bg-voicearchi_purple_glow/10 border border-white/20 transition-transform duration-500 ease-in-out ${
                !constraintsWindowActive ? "hidden" : ""
            }`}
        >
            {/* Tabs for switching views */}
            <div className="w-full flex border-b border-white/20">
                <button
                    className={`flex-1 py-2 text-center text-white transition-all ${
                        activeTab === "constraints" ? "border-b-2 border-voicearchi_purple_bright font-bold" : "opacity-50"
                    }`}
                    onClick={() => setActiveTab("constraints")}
                >
                    Extracted Constraints
                </button>
                <button
                    className={`flex-1 py-2 text-center text-white transition-all ${
                        activeTab === "floorplan" ? "border-b-2 border-voicearchi_purple_bright font-bold" : "opacity-50"
                    }`}
                    onClick={() => setActiveTab("floorplan")}
                >
                    Final Floorplan
                </button>
            </div>

            {/* Loading Animation */}
            <DotLottieReact
                className={`w-100 h-auto top-50 absolute left-1/2 transform -translate-x-1/2 invert ${
                    !isLoadingConstraints ? "hidden" : ""
                }`}
                src="https://lottie.host/b3446f2b-ac55-4666-afc8-439b14425a7a/qMMIJWHNSc.lottie"
                loop
                autoplay
            />

            {/* Content Window */}
            <div className="w-120 h-130 border-b-1 border-b-voicearchi_purple_bright/20 absolute left-1/2 transform -translate-x-1/2 top-14 overflow-auto p-2 text-white rounded-md scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar scrollbar-thumb-voicearchi_purple_glow_dim/15 scrollbar-track-white/0 scrollbar-hover:scrollbar-thumb-voicearchi_purple_glow_dim/30 overflow-y-scroll">
                {activeTab === "constraints" && (
                    <>
                        {error && <p style={{ color: "red" }}>{error}</p>}
                        {extractedData && <JsonViewer data={extractedData} />}
                    </>
                )}
            {activeTab === "floorplan" && (
                <div className="flex justify-center items-center h-full">
                    {floorplanImage ? (
                        <img src={floorplanImage} alt="Final Floorplan" className="w-auto max-h-full rounded-lg shadow-lg" />
                    ) : (
                        <p className="text-center text-white">[Final Floorplan Visualization Here]</p>
                    )}
                </div>
            )}

            </div>

            {/* Finalize Button */}
            {activeTab === "constraints" && (
              <button
                  className={`w-40 rounded-full border-1 border-voicearchi_purple_bright font-montserrat hover:bg-voicearchi_purple_glow/70 absolute left-1/2 transform -translate-x-1/2 bottom-5 ${
                      isLoadingConstraints || isLoadingFinalization ? "hidden" : ""
                  }`}
                  onClick={handleFinalizeFloorplan}
              >
                  {isLoadingFinalization ? "Processing..." : "Finalize Floorplan"}
              </button>
            )}
        </div>
      </>

    );


};

export default CreateFloorplan;