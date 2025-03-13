import React from "react";

const LoginPopup = ({ isOpen, onClose }) => {
  if (!isOpen) return null; // Don't render if not open

  return (
    <div
      className="fixed inset-0 flex items-center justify-center z-50"
      style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }} // Background overlay
    >
      {/* Container for Split Login */}
      <div className="flex w-[700px] h-[400px] bg-white rounded-lg shadow-lg overflow-hidden">
        
        {/* Left Side - Login Form */}
        <div className="w-1/2 p-6 flex flex-col justify-center">
          <h2 className="text-2xl font-bold mb-4 text-center">Log in</h2>
          
          {/* Email Input */}
          <input
            type="text"
            placeholder="Email"
            className="w-full px-4 py-2 border rounded-md mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          {/* Password Input */}
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 border rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          {/* Forgot Password */}
          <p className="text-sm text-gray-600 mb-4 text-center">Forgot your password?</p>

          {/* Buttons */}
          <button className="w-full py-2 bg-voicearchi-blue text-white rounded-md hover:bg-blue-600">
            Login
          </button>
        </div>

        {/* Right Side - Image or Welcome Section */}
        <div
          className="w-1/2 bg-voicearchi-blue flex flex-col justify-center items-center text-white p-6"
          style={{
            backgroundImage: "url('/path-to-your-image.jpg')",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <h2 className="text-xl font-semibold mb-2">Hello, Friend!</h2>
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
