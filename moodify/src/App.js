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
        sequence={[2000, "How is the world feeling today?", 2000]}
        wrapper="h2"
        cursor={true}
        style={{ whiteSpace: "pre-line", display: "block" }}
      />

      <MoodChart />
    </div>
  );
}

export default App;
