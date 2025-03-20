import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styling/LoginPage.css";
import config from '../config';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });
  const navigate = useNavigate();

  useEffect(() => {
    fetchCookie();
  }, []);

  //function for cookies
  const fetchCookie = async () => {
    try {
        const response = await fetch(`${config.apiURL}/cookie`, {
            method: 'GET',
            credentials: 'include'  // Ensure cookies are sent with the request
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Logged-in user:', data.username);
            setUsername(data.username);  // Set username in state
        } else {
            console.log('No cookie found');
        }
    } catch (error) {
        console.error('Error fetching cookie:', error);
    }
  };

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (username.trim() === '' || password.trim() === '') {
      setMessage({ type: 'error', content: 'All fields are required.' });
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
        body: JSON.stringify({ username, password }),
        credentials: 'include' // Include credentials if needed
      });

      if (response.ok) {
        setMessage({ type: 'success', content: 'Authentication successful' });
        console.log('success');
        fetchCookie();
        // setAuthenticated(true); // Uncomment if you have an authentication state
        navigate('/main'); // Redirect to main page after successful authentication
      } else {
        setMessage({ type: 'error', content: 'Authentication failed. Incorrect username or password.' });
      }
    } catch (error) {
      console.error('Error occurred during authentication:', error);
      setMessage({ type: 'error', content: 'Authentication failed. Please try again.' });
    }
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

