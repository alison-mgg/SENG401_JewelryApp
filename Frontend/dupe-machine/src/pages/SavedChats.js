import React, { useState, useEffect } from "react";
import "../styling/SavedChats.css";
import { useAuth } from '../AuthContext';

const SavedChats = () => {
  const [selectedChat, setSelectedChat] = useState(null); // Store the selected chat (response + date)
  const [userChats, setUserChats] = useState([]); // Store all chats (response + date)
  const { username } = useAuth();

  // useEffect hook to fetch user chats whenever the username changes
useEffect(() => {
  // Async function to fetch user chats (images) from the server
  const fetchUserChats = async () => {
    try {
      // Send GET request to fetch user chat data (images) using the username
      const response = await fetch(`http://localhost:5000/api/user/${username}/images`);
      
      // Check if the response is successful
      if (response.ok) {
        const data = await response.json();  // Parse the response data
        
        // Store the fetched chats (response + date) in the state
        setUserChats(data); 
      } else {
        console.error("Failed to fetch user chats");  // Log error if the fetch failed
      }
    } catch (error) {
      console.error("Error fetching user chats:", error);  // Log any network or other errors
    }
  };

  // Only call the fetchUserChats function if username is available
  if (username) {
    fetchUserChats();
  }
}, [username]);  // Dependency array: Runs whenever the username changes

  return (
    <div className="saved-chats-wrapper">
      <div className={`saved-chats-container ${selectedChat ? "dimmed" : ""}`}>
        <div className="saved-chats scrollable">
          {userChats.map((chat, index) => (
            <div key={index} className="chat-item">
              <div
                className="chat-date"
                onClick={() => setSelectedChat(chat)} // Pass the entire chat object (response + date)
              >
                {chat.uploaded_at} {/* Display the date and time */}
              </div>
            </div>
          ))}
        </div>
      </div>
      {selectedChat && (
        <div className="chat-format-overlay">
          <button className="close-button" onClick={() => setSelectedChat(null)}>
            Close
          </button>
          <div className="chat-format-content">
            <div className="chat-textbox">
              <h3>SIMILAR PRODUCTS</h3>
              <p>{selectedChat.response}</p> {/* Display the response */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SavedChats;

