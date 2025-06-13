import React from "react";
import voicearchi_svg_intro_title from "../assets/intro_title_svg.svg";
import voicearchi_svg_floorplan_outer_wall from "../assets/floorplan_outer_wall.svg"
import voicearchi_svg_floorplan_inner_wall from "../assets/floorplan_inner_wall.svg"
import voicearchi_svg_floorplan_diningtable from "../assets/floorplan_diningtable.svg"
import voicearchi_svg_floorplan_bathitems from "../assets/floorplan_bathitems.svg"
import voicearchi_svg_floorplan_sofas from "../assets/floorplan_sofas.svg"
import voicearchi_svg_floorplan_diningtable2 from "../assets/floorplan_diningtable2.svg"
import voicearchi_svg_floorplan_bed1 from "../assets/floorplan_bed1.svg"
import voicearchi_svg_floorplan_bed2 from "../assets/floorplan_bed2.svg"
import voicearchi_svg_floorplan_cabinets from "../assets/floorplan_cabinets.svg"
import voicearchi_svg_floorplan_stairs from "../assets/floorplan_stairs.svg"

const Intro = ({ onGetStarted }) =>{

    return(
        <>
        <div className="relative h-screen w-full flex">
        {/* Main Intro Heading: Design with your voice with VoiceArchi */}
        <img src={voicearchi_svg_intro_title} alt="VoiceArchi Intro Heading" className="h-20 w-auto absolute left-1/2 transform -translate-x-1/2 top-35" />
        {/* Floorplan SVGs */}
        <img src={voicearchi_svg_floorplan_outer_wall} alt="Floorplan SVG" className="animate-scroll-open invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_inner_wall} alt="Floorplan SVG" className="animate-reveal invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_sofas} alt="Floorplan SVG" className="animate-reveal invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_diningtable} alt="Floorplan SVG" className="animate-reveal-reverse invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_diningtable2} alt="Floorplan SVG" className="animate-reveal invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_stairs} alt="Floorplan SVG" className="animate-reveal invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_bed1} alt="Floorplan SVG" className="animate-reveal-reverse invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_bed2} alt="Floorplan SVG" className="animate-reveal-reverse invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_cabinets} alt="Floorplan SVG" className="animate-reveal-reverse invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />
        <img src={voicearchi_svg_floorplan_bathitems} alt="Floorplan SVG" className="animate-reveal invert-100 h-50 w-auto absolute left-1/2 transform -translate-x-1/2 top-70" />

      {/* Main Intro description */}
      <h1 className = "text-gray-100 font-montserrat w-150 h-auto absolute left-1/2 transform -translate-x-1/2 top-140">VoiceArchi transforms your voice commands into 2D floorplans instantly. Simply describe your idea, and our AI-powered system will convert it into a structured design, streamlining the floorplan creation process effortlessly.</h1>
      {/* Get Started Now Button */}
      <button className="hidden absolute left-1/2 transform -translate-x-1/2 top-170 md:block border border-voicearchi_purple_bright text-white px-4 py-1 mb-3 rounded-lg font-montserrat text-xl font-bold hover:bg-voicearchi_purple_glow_dim"
              onClick={onGetStarted}> Get Started</button>
      </div>
      </>
    );

};

export default Intro;