import React from 'react';
import '../styling/UserDisplay.css'; // Import the CSS file

const UserDisplay = () => {
  return (
    <div className="user-display-container">
      <div className="user-display-content">
        <h2>Display Name</h2>
        <h2>Email</h2>
      </div>
      <div className="custom-line"></div> {/* Custom line under the text */}
      <div className="saved-heading">
        <h2>Saved Chats</h2> 
    </div>
    </div>
    

  );
};

export default UserDisplay;