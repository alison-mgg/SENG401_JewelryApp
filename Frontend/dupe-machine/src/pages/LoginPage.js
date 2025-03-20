import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styling/LoginPage.css";
import config from '../config';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (username.trim() === '' || password.trim() === '') {
      displayMessage('error', 'All fields are required.');
      return;
    }

    try {
      const apiUrl = `${config.apiURL}/login`;
      console.log("apiUrl:", apiUrl);
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': window.location.origin, // Add the Origin header
          'X-Requested-With': 'XMLHttpRequest' // Add the X-Requested-With header
        },
        body: JSON.stringify({ username, password })
      });

      if (!response.ok) {
        const data = await response.json();
        displayMessage('error', data.error || 'Authentication failed.');
        return;
      }

      displayMessage('success', 'Login successful!');
      console.log('success');
      navigate('/main');

    } catch (error) {
      displayMessage('error', 'Something went wrong. Please try again later.');
    }
  };

  const displayMessage = (type, content) => {
    setMessage({ type, content });
    setTimeout(() => setMessage({ type: '', content: '' }), 5000);
  };

  return (
    <div className="login-container">
      <div className="loginArea">
        <div className="login-box">
          <h1 className="page-title">Welcome to The Dupe Machine</h1>
          <h2 className="login-title">Login</h2>

          {message.content && (
            <div className={`message-box ${message.type}`}>
              <p>{message.content}</p>
            </div>
          )}

          <form className="login-form">
            <div className="input-group">
              <input
                type="text"
                placeholder="Username"
                className="input-field"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                placeholder="Password"
                className="input-field"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button className="login-button" onClick={handleSubmit}>Login</button>
          </form>
          <h3 className="no-account-title">Don't have an account?</h3>
          <div className="options">
            <Link to="/signup">
              <button className="signup-button">Sign Up</button>
            </Link>
            <Link to="/main">
              <button className="guest-button">Continue as Guest</button>
            </Link>
          </div>
        </div>
        <div className="loginImage"></div>
      </div>
    </div>
  );
}

export default LoginPage;

