import React, { useState } from "react";
import "../styling/InputBox.css";

function InputBox() {
  const [inputText, setInputText] = useState("");
  const [response, setResponse] = useState(""); // State to store the backend response

  const handleSave = async () => {
    if (!inputText.trim()) {
      console.log("No input provided.");
      return;
    }
  
    console.log("Sending request with:", inputText);
  
    try {
      const response = await fetch("http://localhost:5000/analyze_text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });
  
      console.log("Received response:", response);
  
      const data = await response.json();
      console.log("Response JSON:", data);
  
      setResponse(data.description || "No description found.");
    } catch (error) {
      console.error("Error fetching data:", error);
      setResponse("Error analyzing text.");
    }
  };

  const handleUpload = () => {
    setInputText("");
    setResponse(""); // Clear response when input is reset
    console.log("Uploaded:", inputText);
  };

  return (
    <div className="Input-Container">
      <div className="input-wrapper">
        <button className="icon-buttonIB" onClick={handleSave}>
          &#10084;&#65039;
        </button>
        <textarea
          className="text-input"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter your text here..."
        />
        <button className="icon-buttonIB" onClick={handleUpload}>
          &#8593;
        </button>
      </div>
      {response && (
        <div className="response-box">
          <h3>Analysis Result:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default InputBox;
