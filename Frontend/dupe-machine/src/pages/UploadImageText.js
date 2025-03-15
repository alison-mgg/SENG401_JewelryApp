import React, { useState } from "react";
import "../styling/UploadImageText.css";

function UploadImageText() {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submittedContent, setSubmittedContent] = useState(null);
  const [inputText, setInputText] = useState("");
  const [image, setImage] = useState(null);

  const handleTextSubmit = () => {
    setSubmittedContent(inputText);
    setIsSubmitted(true);
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setSubmittedContent(URL.createObjectURL(file));
      setIsSubmitted(true);
    }
  };

  const handleNewSubmission = () => {
    setIsSubmitted(false);
    setInputText("");
    setImage(null);
  };

  const triggerFileInput = () => {
    document.getElementById("imageUpload").click();
  };

  return (
    <div className="TextImage-Container">
      {!isSubmitted ? (
        <div className="input-wrapperUIT">
          <div className="text-image-box">
            <h2>Choose to upload text or an image:</h2>
            <div className="buttons-container">
              <div className="upload-image">
                <button className="image-button" onClick={triggerFileInput}>&#128247;</button>
                <input
                  type="file"
                  id="imageUpload"
                  onChange={handleImageUpload}
                  style={{ display: "none" }}
                />
              </div>

              <div className="upload-text">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Enter text here..."
                />
                <button className="text-button" onClick={handleTextSubmit}>&#8593;</button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="submitted-content">
          {submittedContent && !image ? (
            <div className="text-display">
              <p>{submittedContent}</p>
            </div>
          ) : (
            <div className="image-display">
              <img src={submittedContent} alt="Uploaded" />
            </div>
          )}
          <button className="newSub-button"onClick={handleNewSubmission}>New Submission</button>
        </div>
      )}
    </div>
  );
}

export default UploadImageText;
