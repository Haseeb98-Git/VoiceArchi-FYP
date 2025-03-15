import React, { useState } from "react";
import voicearchi_svg_logo from "../assets/logo_svg.svg";
import LoginPopup from "../components/LoginPopup";

const Navbar = () => {
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    return (
        <>
        {/* Navbar */}
        <nav className="brightness-150 fixed z-50 top-0 left-0 w-full h-22 flex items-center px-4 md:px-8 justify-between">
            <div className="flex items-center px-15">
            <img src={voicearchi_svg_logo} alt="VoiceArchi Logo" className="h-7 w-auto" />
            </div>
            <div className="absolute left-1/2 transform -translate-x-1/2 hidden md:flex space-x-6">
            <button className="text-white font-montserrat transition-all duration-200 hover:text-lg">Intro</button>
            <button className="text-white font-montserrat transition-all duration-200 hover:text-lg">About</button>
            <button className="text-white font-montserrat transition-all duration-200 hover:text-lg">Features</button>
            <button className="text-white font-montserrat transition-all duration-200 hover:text-lg">Showcase</button>
            <button className="text-white font-montserrat transition-all duration-200 hover:text-lg">Contact Us</button>
            </div>
            <div className="flex items-center">
            <button onClick={() => setIsLoginOpen(true)} className="hidden mr-10 md:block border border-voicearchi-blue text-white px-4 py-1 mb-3 rounded-lg font-montserrat hover:bg-voicearchi_purple_glow_dim">
                Login
            </button>
            <button className="md:hidden text-white focus:outline-none ml-4" onClick={() => setIsOpen(!isOpen)}>
                ☰
            </button>
            </div>
        </nav>

        <LoginPopup isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} />
        </>
    );
};

export default Navbar;