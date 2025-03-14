import React, {useState} from "react";
import Intro from "../components/Intro";


const Home = () =>{
    let loggedIn = false;
    const [isMoved, setIsMoved] = useState(false);
    return (
        <>

    {loggedIn?

    <>
    {/* Content when the user is not logged in. */}

    {/* Main Background */}
      <div className="relative w-full max-w-full overflow-hidden bg-voicearchi_dark_background text-white">

        {/* Glowing Effects (Do Not Remove) */}
        <div className="absolute left-1/2 transform -translate-x-1/2 -top-60 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
        <div className="absolute left-1/2 transform -translate-x-1/2 bottom-500 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
        {/* <div className="absolute top-180 -left-160 w-[800px] h-[700px] bg-voicearchi_purple_glow/50 blur-[300px] rounded-full pointer-events-none"></div>
        <div className="absolute top-450 -right-160 w-[800px] h-[700px] bg-voicearchi_purple_glow/50 blur-[300px] rounded-full pointer-events-none"></div>
        <div className="absolute top-750 -left-160 w-[800px] h-[700px] bg-voicearchi_purple_glow/50 blur-[300px] rounded-full pointer-events-none"></div> */}

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
            <div className="relative w-full h-screen max-w-full overflow-hidden bg-voicearchi_dark_background text-white">
            {/* Glowing Effects (Do Not Remove) */}
            <div className="absolute left-1/2 transform -translate-x-1/2 -top-60 w-[4000px] h-[800px] bg-voicearchi_purple_glow/20 blur-[300px] rounded-full pointer-events-none"></div>
            <div className="absolute top-180 -left-160 w-[1000px] h-[800px] bg-voicearchi_purple_glow/0 blur-[1000px] rounded-full pointer-events-none"></div>
            {/* Chat box*/}
                <button
                  onClick={() => setIsMoved(!isMoved)}
                  className="hidden absolute top-20 left-80 px-4 py-2 bg-white text-black rounded-md"
                >
                  Move Chat Box
                </button>

                <div
                  className={`w-140 h-160 rounded-xl absolute left-1/2 transform -translate-x-1/2 top-30 bg-voicearchi_purple_glow/10 border border-white/20 transition-transform duration-500 ease-in-out ${
                    isMoved ? "translate-x-32" : ""
                  }`}
                >
                  {/*Chat title*/}
                  <h1 className="absolute left-1/2 transform -translate-x-1/2 text-white">
                    Chat
                  </h1>
                  {/*Chat bar*/}
                  <div className="absolute left-1/2 transform -translate-x-1/2 bottom-5 w-100 h-auto">
                  <input
                      type="text"
                      placeholder="Type your message"
                      className="w-full px-4 py-2 rounded-3xl border border-gray-300/30 focus:border-voicearchi_purple_bright focus:outline-none focus:ring-blue-500 text-gray-100"
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