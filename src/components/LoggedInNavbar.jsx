import React from "react";
import voicearchi_svg_logo from "../assets/logo_svg.svg";
import profile_generic_icon from "../assets/profile_generic_icon.svg";
import dashboard_icon from "../assets/dashboard_icon.svg";
import create_floorplan_icon from "../assets/create_floorplan_icon.svg";
import my_floorplans_icon from "../assets/my_floorplans_icon.svg";
import my_ideas_icon from "../assets/my_ideas_icon.svg";
import settings_icon from "../assets/settings_icon.svg";
import help_icon from "../assets/help_icon.svg";

const LoggedInNavbar = () => {

    return (
        <>
        {/* Logged in Navbar */}
        <nav className="fixed z-50 top-0 left-0 w-full h-22 flex items-center px-4 md:px-8 justify-between">
            <div className="flex items-center px-15">
            <img src={voicearchi_svg_logo} alt="VoiceArchi Logo" className="h-7 w-auto" />
            </div>
            <div className="absolute left-1/2 transform -translate-x-1/2 hidden md:flex space-x-6">
            <button className="text-white font-montserrat text-xl transition-all duration-200">User Dashboard</button>
            </div>
            <div className="flex items-center">
            <h3 className="text-gray-100 pr-5 font-montserrat">Haseeb Ali</h3>
            <img src={profile_generic_icon} className="w-7 h-auto rounded-2xl border-1 border-white hover:bg-voicearchi_purple_glow_dim"/>
            </div>
        </nav>
        
        {/*Side Navbar*/}
        <nav className = "fixed z-50 top-50 left-15 h-70 flex flex-col items-start justify-between">
            <div className = "flex flex-col items-start">
            <img src={dashboard_icon} className="w-30 h-auto py-2 transition-all duration-200 hover:w-33"/>
            <img src={create_floorplan_icon} className="w-44 h-auto px-0.5 py-2 transition-all duration-200 hover:w-48"/>
            <img src={my_floorplans_icon} className="w-37 h-auto py-2 transition-all duration-200 hover:w-41"/>
            <img src={my_ideas_icon} className="w-26 h-auto px-0.5 py-2 transition-all duration-200 hover:w-29"/>
            </div>
            
            <div className = "flex flex-col items-start">
            <img src={settings_icon} className="w-25 h-auto py-2 transition-all duration-200 hover:w-27"/>
            <img src={help_icon} className="w-17 px-1 h-auto py-2 transition-all duration-200 hover:w-19"/>

            </div>
        </nav>
        </>
    );
};

export default LoggedInNavbar;