import Navbar from "./components/Navbar";
import { useState } from "react";
import Home from "./components/Home";
import LoggedInNavbar from "./components/LoggedInNavbar";
import "./App.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(false); // useState hook
  return (
    <>
    {/* Injecting Navbar Component */}
    {!loggedIn? <Navbar/>: <LoggedInNavbar/>}
     <Home loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
    </>
  );
}

export default App;