import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styling/ProfilePage.css";
import NavBar from "./NavigationBar.js";

function ProfilePage() {

  return (
    <div className="profilepage-container">
     <NavBar />
    <h1 className="page-title">Test: ProfilePage</h1>
    </div>
);
}

export default ProfilePage;