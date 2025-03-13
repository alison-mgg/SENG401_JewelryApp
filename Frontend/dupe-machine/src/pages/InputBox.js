import React, { useState } from "react";
import "../styling/InputBox.css";

function InputBox() {
  const [inputText, setInputText] = useState("");

  const handleSave = () => {
    // Implement saving functionality
    console.log("Saved:", inputText);
  };

  const handleUpload = () => {
    // Clear the input box when the up arrow is clicked
    setInputText("");
    console.log("Uploaded:", inputText);
  };

  return (
    <div className="Input-Container">
      <div className="input-wrapper">
        <button className="icon-button" onClick={handleSave}>
          &#10084;&#65039; {/* Heart emoji using HTML code */}
        </button>
        <textarea
          className="text-input"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter your text here..."
        />
        <button className="icon-button" onClick={handleUpload}>
          &#8593; {/* Up arrow using HTML code */}
        </button>
      </div>
    </div>
  );
}

export default InputBox;
