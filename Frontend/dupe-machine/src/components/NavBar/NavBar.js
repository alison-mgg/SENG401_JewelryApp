import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css"; // Updated import path to match the same folder

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/">Home</Link>
              </div>
      <div className="navbar-right">
        <Link to="/profile">Profile</Link>
      </div>
    </nav>
  );
}

export default NavBar;
