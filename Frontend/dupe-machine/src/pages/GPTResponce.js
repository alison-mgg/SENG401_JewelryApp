import React, { useState, useEffect } from "react";
import "../styling/GPTResponce.css";

function GPTResponce() {
  const [lines, setLines] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const promptResponse = await fetch("/TestPrompt.txt");
        const geminiResponse = await fetch("/TestGemini.txt");
        
        const promptText = await promptResponse.text();
        const geminiText = await geminiResponse.text();
        
        const promptLines = promptText.split("\n");
        const geminiLines = geminiText.split("\n");

        const maxLines = Math.max(promptLines.length, geminiLines.length);
        const combinedLines = [];

        for (let i = 0; i < maxLines; i++) {
          if (geminiLines[i]) combinedLines.push({ text: geminiLines[i], align: "left" });
          if (promptLines[i]) combinedLines.push({ text: promptLines[i], align: "right" });
        }

        setLines(combinedLines);
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="TextImage-Container">
      <div className="scrollable-box">
        {lines.map((line, index) => (
          <p key={index} className={line.align === "left" ? "align-left" : "align-right"}>
            {line.text}
          </p>
        ))}
      </div>
    </div>
  );
}

export default GPTResponce;

