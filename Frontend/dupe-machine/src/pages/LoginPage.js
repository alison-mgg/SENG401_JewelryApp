import React from "react";
import { Link } from "react-router-dom";
import "../styling/LoginPage.css";

function LoginPage() {
  return (
    <div className="login-container">
      <h1 className="page-title">Welcome to The Dupe Machine</h1>
      <h2 className="login-title">Login</h2>
      <div className="login-box">
        <input type="text" placeholder="Username" className="input-field" />
        <input type="password" placeholder="Password" className="input-field" />
        <button className="login-button">Login</button>
      </div>
      <h3 className="no-account-title">Don't have an account?</h3>
      <div className="options">
        <Link to="/signup">
          <button className="signup-button">Sign Up</button>
        </Link>
        <Link to= "/main">
        <button className="guest-button">Continue as Guest</button>
        </Link>
      </div>
    </div>
  );
}

export default LoginPage;
