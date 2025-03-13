import Navbar from "./components/Navbar";
import Home from "./components/Home";
import LoggedInNavbar from "./components/LoggedInNavbar";
import "./App.css";

function App() {
let loggedIn = false;
  return (
    <>
    {/* Injecting Navbar Component */}
    {loggedIn? <Navbar/>: <LoggedInNavbar/>}
     <Home/>
    </>
  );
}

export default App;