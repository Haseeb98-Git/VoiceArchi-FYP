import React from "react";
import voicearchi_svg_logo from "../assets/logo_svg.svg";

const LoginPopup = ({ isOpen, onClose }) => {
  if (!isOpen) return null; // Don't render if not open

  return (
    <div
      className="fixed inset-0 flex items-center justify-center z-50"
      style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }} // Background overlay
    >
      {/* Container for Split Login */}
      <div className="flex w-[700px] h-[400px] bg-gray-50 rounded-lg shadow-lg overflow-hidden">
        
        {/* Left Side - Login Form */}
        <div className="w-1/2 p-6 flex flex-col justify-center">
          <h2 className="text-2xl font-bold mb-4 text-center">Log in</h2>
          
          {/* Email Input */}
          <input
            type="text"
            placeholder="Email"
            className="w-full px-4 py-2 border rounded-md mb-2 focus:outline-none focus:ring-2 focus:ring-voicearchi_purple_bright"
          />
          
          {/* Password Input */}
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 border rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-voicearchi_purple_bright"
          />
          
          {/* Forgot Password */}
          <p className="text-sm text-gray-600 mb-4 text-center">Forgot your password?</p>

          {/* Buttons */}
          <button className="w-full py-2 bg-voicearchi_purple_glow text-white rounded-md hover:bg-voicearchi_purple_glow_dim">
            Login
          </button>
        </div>

        {/* Right Side - Image or Welcome Section */}
        <div
          className="w-1/2 bg-slate-500 flex flex-col justify-center items-center text-white p-6"
        >
          <h2 className="text-xl font-semibold mb-2">Don't have an account?</h2>
          <p className="text-center text-sm mb-4">
            Enter your details to start your journey with us.
          </p>
          <button className="px-4 py-2 border border-white rounded-md hover:bg-white hover:text-blue-600 transition">
            Sign Up
          </button>
        </div>

      </div>
    </div>
  );
};

export default LoginPopup;
