import React, { useEffect, useState } from "react";
import "../styling/ProfilePage.css";
import NavBar from "./NavigationBar.js";
import UserDetails from "./UserDisplay.js";
import Chats from "./SavedChats.js";
import { useAuth } from '../AuthContext'; // Import useAuth to get the current user
import { useNavigate } from 'react-router-dom'; // Import useNavigate for redirection

function ProfilePage() {
  const [userData, setUserData] = useState({ username: "", email: "" });
  const { isAuthenticated, username, logout } = useAuth(); // Get the current username and logout function from AuthContext
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    if (isAuthenticated && username) {
      // Fetch user data from the backend
      const fetchUserData = async () => {
        try {
          const response = await fetch(`http://localhost:5000/api/user/${username}`);
          if (response.ok) {
            const data = await response.json();
            setUserData({ username: data.username, email: data.email });
          } else {
            console.error("Failed to fetch user data");
          }
        } catch (error) {
          console.error("Error fetching user data:", error);
        }
      };

      fetchUserData();
    }
  }, [isAuthenticated, username]);

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        credentials: 'include', // Include cookies in the request
      });

      if (response.ok) {
        logout(); // Call the logout function from AuthContext
        navigate('/'); // Redirect to the login page
      } else {
        console.error("Failed to logout");
      }
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <div className="profilepage-container">
      <NavBar />
      <UserDetails username={userData.username} email={userData.email} />
      <Chats />
      <button onClick={handleLogout} className="logout-button">Logout</button>
    </div>
  );
}

export default ProfilePage;