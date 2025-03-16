import React from "react";
import Intro from "../components/Intro";
import background_pattern from "../assets/background_pattern_1.svg"
import CreateFloorplan from "./CreateFloorplan";
const Home = () =>{

    let loggedIn = false;

    return (
        <>

    {loggedIn?

    <>

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

            {/*Create Floorplan Component*/}
            <CreateFloorplan/>
            </div>

      </>
      }
        </>

    );


};

export default Home;