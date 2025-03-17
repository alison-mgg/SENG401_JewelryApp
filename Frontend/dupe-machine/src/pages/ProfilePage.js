import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styling/ProfilePage.css";
import NavBar from "./NavigationBar.js";
import UserDetails from "./UserDisplay.js";
import Chats from "./SavedChats.js";

function ProfilePage() {

  return (
    <div className="profilepage-container">
     <NavBar />
    <UserDetails/>
    <Chats />
    </div>
);
}


export default ProfilePage;