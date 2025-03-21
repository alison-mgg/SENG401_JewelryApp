import React, { useState, useEffect } from "react";
import "../styling/SavedChats.css";
import { useAuth } from '../AuthContext';

const SavedChats = () => {
  const [selectedChat, setSelectedChat] = useState(null); // Store the selected chat (response + date)
  const [userChats, setUserChats] = useState([]); // Store all chats (response + date)
  const { username } = useAuth();

  useEffect(() => {
    const fetchUserChats = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/user/${username}/images`);
        if (response.ok) {
          const data = await response.json();
          setUserChats(data); // Store the chats (response + date)
        } else {
          console.error("Failed to fetch user chats");
        }
      } catch (error) {
        console.error("Error fetching user chats:", error);
      }
    };

    if (username) {
      fetchUserChats();
    }
  }, [username]);

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
              <h3>Response:</h3>
              <p>{selectedChat.response}</p> {/* Display the response */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SavedChats;

// import React, { useState, useEffect } from "react";
// import "../styling/SavedChats.css";
// import "../styling/ChatFormatProfile.css";
// import { useAuth } from '../AuthContext';

// const SavedChats = () => {
//   const [selectedChat, setSelectedChat] = useState(null); // Store the selected chat (image + description)
//   const [userChats, setUserChats] = useState([]); // Store all chats (image + description)
//   const { username } = useAuth();

//   useEffect(() => {
//     const fetchUserChats = async () => {
//       try {
//         const response = await fetch(`http://localhost:5000/api/user/${username}/images`);
//         if (response.ok) {
//           const data = await response.json();
//           setUserChats(data); // Store the chats (image + description)
//         } else {
//           console.error("Failed to fetch user chats");
//         }
//       } catch (error) {
//         console.error("Error fetching user chats:", error);
//       }
//     };

//     if (username) {
//       fetchUserChats();
//     }
//   }, [username]);

//   return (
//     <div className="saved-chats-wrapper">
//       <div className={`saved-chats-container ${selectedChat ? "dimmed" : ""}`}>
//         <div className="saved-chats scrollable">
//           {userChats.map((chat, index) => (
//             <div key={index} className="chat-item">
//               <img
//                 src={`http://localhost:5000${chat.img_path}`} // Use the full URL returned by the backend
//                 alt={`Chat ${index}`}
//                 className="chat-image"
//                 onClick={() => setSelectedChat(chat)} // Pass the entire chat object (image + description)
//               />
//             </div>
//           ))}
//         </div>
//       </div>
//       {selectedChat && (
//         <ChatFormatProfile
//           image={selectedChat.img_path}
//           description={selectedChat.response} // Pass the description to ChatFormatProfile
//           onClose={() => setSelectedChat(null)}
//         />
//       )}
//     </div>
//   );
// };

// const ChatFormatProfile = ({ image, description, onClose }) => {
//   return (
//     <div className="chat-format-overlay">
//       <button className="close-button" onClick={onClose}>X</button>
//       <div className="chat-format-content">
//         <img src={`http://localhost:5000${image}`} alt="Selected Chat" className="enlarged-image" />
//         <div className="chat-textbox">
//           <h3>Description:</h3>
//           <p>{description}</p> {/* Display the description */}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default SavedChats;