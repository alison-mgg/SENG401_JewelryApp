import React, { useState } from "react";
import "../styling/SavedChats.css";
import "../styling/ChatFormatProfile.css";

const imageContext = require.context("./testImages", false, /\.(png|jpe?g)$/);
const images = imageContext.keys().map(imageContext);

const SavedChats = () => {
  const [selectedImage, setSelectedImage] = useState(null);

  return (
    <div className="saved-chats-wrapper">
      <div className={`saved-chats-container ${selectedImage ? "dimmed" : ""}`}>
        <div className="saved-chats scrollable">
          {images.map((src, index) => (
            <img
              key={index}
              src={src}
              alt={`Chat ${index}`}
              className="chat-image"
              onClick={() => setSelectedImage(src)}
            />
          ))}
        </div>
      </div>
      {selectedImage && (
        <ChatFormatProfile
          image={selectedImage}
          onClose={() => setSelectedImage(null)}
        />
      )}
    </div>
  );
};

const ChatFormatProfile = ({ image, onClose }) => {
  return (
    <div className="chat-format-overlay">
      <button className="close-button" onClick={onClose}>X</button>
      <div className="chat-format-content">
        <img src={image} alt="Selected Chat" className="enlarged-image" />
        <div className="chat-textbox">Sample text displayed here</div>
      </div>
    </div>
  );
};

export default SavedChats;