import React from "react";
import { TypeAnimation } from "react-type-animation";
import MoodChart from "./MoodChart";

function App() {
  return (
    <div style={{
      background: "#000",
      color: "#fff",
      height: "100vh",
      padding: "2rem",
      fontFamily: "Cutive Mono, monospace"
    }}>
      <TypeAnimation
        sequence={["Moodify", 1000]}
        wrapper="h1"
        cursor={true}
        style={{ whiteSpace: "pre-line", display: "block" }}
      />
      <TypeAnimation
        sequence={[ "How is the world feeling today?"]}
        wrapper="h2"
        cursor={true}
        style={{ whiteSpace: "pre-line", display: "block" }}
      />
    {/* Top-right button */}
    <a 
      href="/faq" 
      style={{
        position: "absolute",
        top: "20px",
        right: "20px",
        padding: "10px 20px",
        backgroundColor: "#fff",
        color: "#000",
        fontFamily: "Cutive Mono, monospace",
        fontSize: "16px",
        fontWeight: "bold",
        border: "2px solid #fff",
        borderRadius: "6px",
        textDecoration: "none",
        cursor: "pointer",
        transition: "0.3s",
      }}
      onMouseEnter={(e) => {
        e.target.style.backgroundColor = "#000";
        e.target.style.color = "#fff";
      }}
      onMouseLeave={(e) => {
        e.target.style.backgroundColor = "#fff";
        e.target.style.color = "#000";
      }}
    >
      What is this?
    </a>
      <MoodChart />
    </div>
  );
}

export default App;
