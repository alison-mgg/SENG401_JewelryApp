import React, { useEffect, useState } from "react";
import "../styling/ProfilePage.css";
import NavBar from "./NavigationBar.js";
import UserDetails from "./UserDisplay.js";
import Chats from "./SavedChats.js";
import { useAuth } from '../AuthContext'; 
import { useNavigate } from 'react-router-dom'; 

function ProfilePage() {
  const [userData, setUserData] = useState({ username: "", email: "" });
  const { isAuthenticated, username, logout } = useAuth();
  const navigate = useNavigate(); 

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/signup'); // Redirect to the signup page if not authenticated
    }
  }, [isAuthenticated, navigate]);

// useEffect hook to fetch user data when authenticated and username is available
useEffect(() => {
  if (isAuthenticated && username) {
    // Async function to fetch user data from the server
    const fetchUserData = async () => {
      try {
        // Send GET request to fetch user data using the username
        const response = await fetch(`http://localhost:5000/api/user/${username}`);
        
        // Check if the response is successful
        if (response.ok) {
          const data = await response.json();  // Parse the response data
          
          // Update the state with the user data (username and email)
          setUserData({ username: data.username, email: data.email });
        } else {
          console.error("Failed to fetch user data");  // Log error if the fetch failed
        }
      } catch (error) {
        console.error("Error fetching user data:", error);  // Log any network or other errors
      }
    };

    fetchUserData();  // Call the function to fetch user data
  }
}, [isAuthenticated, username]);  // Dependency array: Runs whenever isAuthenticated or username changes

// handleLogout function to log the user out and redirect them to the login page
const handleLogout = async () => {
  try {
    // Send POST request to logout the user (using cookies for session management)
    const response = await fetch('http://localhost:5000/api/logout', {
      method: 'POST',
      credentials: 'include',  // Include cookies (session) in the request
    });

    // Check if the logout request was successful
    if (response.ok) {
      logout();  // Call logout function from AuthContext to clear user session
      navigate('/');  // Redirect to the login page after successful logout
    } else {
      console.error("Failed to logout");  // Log error if the logout failed
    }
  } catch (error) {
    console.error("Error logging out:", error);  // Log any network or other errors during logout
  }
};


  return isAuthenticated ? (
    <div className="profilepage-container">
      <NavBar />
      <UserDetails username={userData.username} email={userData.email} />
      <Chats />
      <button onClick={handleLogout} className="logout-button">Logout</button>
    </div>
  ) : null;
}

export default ProfilePage;