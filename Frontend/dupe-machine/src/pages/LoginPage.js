import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from '../AuthContext';
import "../styling/LoginPage.css";

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' }); 
  const { isAuthenticated, login } = useAuth(); 
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to the main page if the user is already authenticated
    if (isAuthenticated) {
      navigate('/main');
    }
  }, [isAuthenticated, navigate]);
  
  useEffect(() => {
    // Fetch the authentication cookie when the component mounts
    fetchCookie();
  }, []);
  
  // Function to fetch the cookie from the server to check if the user is logged in
  const fetchCookie = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/cookie', {
        method: 'GET',
        credentials: 'include' // Include credentials (cookie) in the request
      });
  
      if (response.ok) {
        // If the cookie exists, parse and set the username
        const data = await response.json();
        console.log('Logged-in user:', data.username);
        setUsername(data.username); // Set the username from the cookie
        login(data.username); // Call login function with username
        //console.log('isAuthenticated set to true'); // DEBUG CODE: Log the state change
      } else {
        // If no cookie is found, log the message
        console.log('No cookie found');
      }
    } catch (error) {
      // Catch any errors during the fetch and log them
      console.error('Error fetching cookie:', error);
    }
  };
  
  // Function to handle form submission (login)
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Check if username or password is empty, display error message if true
    if (username.trim() === '' || password.trim() === '') {
      displayMessage('error', 'Username and password are required.');
      return;
    }
  
    try {
      // Send POST request to authenticate the user
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }), // Send username and password in the request body
        credentials: 'include' // Include credentials (cookie) in the request
      });
  
      if (response.ok) {
        // If login is successful, display success message and redirect to main page
        setMessage({ type: 'success', content: 'Authentication successful' });
        console.log('success');
        fetchCookie(); // Fetch the cookie after successful login
        navigate('/main'); // Redirect to main page
      } else {
        // If authentication fails, display an error message
        setMessage({ type: 'error', content: 'Authentication failed. Incorrect username or password.' });
      }
    } catch (error) {
      // Catch any errors during login and display error message
      console.error('Error occurred during authentication:', error);
      setMessage({ type: 'error', content: 'Authentication failed. Please try again.' });
    }
  };
  
  // Function to display messages (success or error) on the UI
  const displayMessage = (type, content) => {
    setMessage({ type, content }); // Set the message
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