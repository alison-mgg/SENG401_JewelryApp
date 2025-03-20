import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
//import { useAuthContext } from '../App.js';
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
//import { useAuthContext } from '../App.js';
import "../styling/LoginPage.css";

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' }); // State to manage the message
  //const { setAuthenticated } = useAuthContext(); // Access setAuthenticated function from context
  const navigate = useNavigate();

  const handleSubmit = async (e) =>{
    e.preventDefault()

    if (username.trim() === '' || password.trim() === '') {
        displayMessage('error', 'Username and password are required.');
        return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/login', { 
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
      });
      if (response.ok) {
        setMessage({ type: 'success', content: 'Authentication successful' });
        console.log('success')
        //setAuthenticated(true);
        navigate('/main'); // Redirect to main page after successful authentication
      } else {
          setMessage({ type: 'error', content: 'Authentication failed. Incorrect username or password.' });
      }
  } catch (error) {
    console.error('Error occurred during authentication:', error);
    setMessage({ type: 'error', content: 'Authentication failed. Please try again.' });
  }

  };

  const displayMessage = (type, content) => {
    setMessage({ type, content });
    setTimeout(() => setMessage({ type: '', content: '' }), 50000); // Clear the message after 50 seconds
  };  


  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' }); // State to manage the message
  //const { setAuthenticated } = useAuthContext(); // Access setAuthenticated function from context
  const navigate = useNavigate();

  const handleSubmit = async (e) =>{
    e.preventDefault()

    if (username.trim() === '' || password.trim() === '') {
        displayMessage('error', 'Username and password are required.');
        return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/login', { 
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
      });
      if (response.ok) {
        setMessage({ type: 'success', content: 'Authentication successful' });
        console.log('success')
        //setAuthenticated(true);
        navigate('/main'); // Redirect to main page after successful authentication
      } else {
          setMessage({ type: 'error', content: 'Authentication failed. Incorrect username or password.' });
      }
  } catch (error) {
    console.error('Error occurred during authentication:', error);
    setMessage({ type: 'error', content: 'Authentication failed. Please try again.' });
  }

  };

  const displayMessage = (type, content) => {
    setMessage({ type, content });
    setTimeout(() => setMessage({ type: '', content: '' }), 50000); // Clear the message after 50 seconds
  };  


  return (
    <div className="login-container">
      <div className="loginArea">
        <div className="login-box">
          <h1 className="page-title">Welcome to The Dupe Machine</h1>
          <h2 className="login-title">Login</h2>
  
          {/* Display message if it exists */}
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
            <button className="login-button" onClick={handleSubmit}>
              Login
            </button>
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

