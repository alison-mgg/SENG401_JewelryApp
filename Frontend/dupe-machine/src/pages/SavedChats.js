import React, { useState, useEffect } from "react";
import "../styling/SavedChats.css";
import "../styling/ChatFormatProfile.css";
import { useAuth } from '../AuthContext';

const SavedChats = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [userImages, setUserImages] = useState([]);
  const { username } = useAuth();

  useEffect(() => {
    const fetchUserImages = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/user/${username}/images`);
        if (response.ok) {
          const data = await response.json();
          setUserImages(data.map(img => img.img_path));
        } else {
          console.error("Failed to fetch user images");
        }
      } catch (error) {
        console.error("Error fetching user images:", error);
      }
    };

    if (username) {
      fetchUserImages();
    }
  }, [username]);

  return (
    <div className="saved-chats-wrapper">
      <div className={`saved-chats-container ${selectedImage ? "dimmed" : ""}`}>
        <div className="saved-chats scrollable">
          {userImages.map((src, index) => (
            <img
              key={index}
              src={`http://localhost:5000${src}`}  // Use the full URL returned by the backend
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
        <img src={`http://localhost:5000${image}`} alt="Selected Chat" className="enlarged-image" />
        <div className="chat-textbox">Sample text displayed here</div>
      </div>
    </div>
  );
};

export default SavedChats;