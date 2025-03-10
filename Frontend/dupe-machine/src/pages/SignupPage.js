import React from "react";
import { Link } from "react-router-dom";
import "../styling/SignupPage.css";

function SignupPage() {
  return (
    <div className="login-container">
      <h1 className="page-title">Welcome to The Dupe Machine</h1>
      <h2 className="login-title">Sign Up</h2>
      <div className="login-box">
        <input type="text" placeholder="Username" className="input-field" />
        <input type="email" placeholder="Email" className="input-field" />
        <input type="password" placeholder="Password" className="input-field" />
        <button className="login-button">Sign Up</button>
      </div>
      <h3 className="no-account-title">Already have an account?</h3>
      <div className="options">
        <Link to="/">
          <button className="signup-button">Login</button>
        </Link>
        <Link to= "/main">
        <button className="guest-button">Continue as Guest</button>
        </Link>
      </div>
    </div>
  );
}

export default SignupPage;