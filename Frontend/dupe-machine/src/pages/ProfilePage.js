import React, { useEffect, useState } from "react";
import "../styling/ProfilePage.css";
import NavBar from "./NavigationBar.js";
import UserDetails from "./UserDisplay.js";
import Chats from "./SavedChats.js";
import { useAuth } from '../AuthContext'; // Import useAuth to get the current user

function ProfilePage() {
  const [userData, setUserData] = useState({ username: "", email: "" });
  const { isAuthenticated, username } = useAuth(); // Get the current username from AuthContext

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

  return (
    <div className="profilepage-container">
      <NavBar />
      <UserDetails username={userData.username} email={userData.email} />
      <Chats />
    </div>
  );
}

export default ProfilePage;