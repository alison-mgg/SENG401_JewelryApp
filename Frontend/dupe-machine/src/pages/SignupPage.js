import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styling/SignupPage.css";
import config from '../config';

function SignupPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (username.trim() === '' || password.trim() === '' || email.trim() === '') {
      displayMessage('error', 'All fields are required.');
      return;
    }

    if (email && email.trim() !== '' && !isValidEmail(email)) {
      displayMessage('error', 'Invalid email format');
      return;
    }

    try {
      const apiUrl = new URL('/signup', config.apiURL).toString();
      console.log("apiUrl:", apiUrl);
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, email })
      });

      if (!response.ok) {
        const data = await response.json();
        displayMessage('error', data.error || 'Signup failed.');
        return;
      }

      displayMessage('success', 'Signup successful!');
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

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  return (
    <div className="login-container">
      <div className="loginArea">
        <div className="login-box">
          <h1 className="page-title">Welcome to The Dupe Machine</h1>
          <h2 className="login-title">Sign Up</h2>

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
                type="email"
                placeholder="Email"
                className="input-field"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
            <button className="login-button" onClick={handleSubmit}>Sign Up</button>
          </form>
          <h3 className="no-account-title">Already have an account?</h3>
          <div className="options">
            <Link to="/">
              <button className="signup-button">Login</button>
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

export default SignupPage;