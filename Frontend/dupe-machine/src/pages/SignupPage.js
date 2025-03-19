import React, { useState }from "react";
import { Link } from "react-router-dom";
import "../styling/SignupPage.css";

// Import config file
import config from '../config';

function SignupPage() {

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if all fields are filled
    if (username.trim() === '' || password.trim() === '' || email.trim() === '') {
      displayMessage('error', 'All fields are required.');
      return;
    }

    // Check if email is valid
    if (email && email.trim() !== '' && !isValidEmail(email)) {
        displayMessage('error', 'Invalid email format');
        return;
    }

    // Send request to backend
    try {
      const response = await fetch(`${config.corsProxyURL}${config.apiURL}/signup`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password, email })
      });
    
      // Check if response is ok
      if (!response.ok) {
        const data = await response.json();
        displayMessage('error', data.error || 'Signup failed.');
        return;
      }

      // If response is ok, display success message
      displayMessage('success', 'Signup successful!');
      console.log('success')

      // Response error
    } catch (error) {
      displayMessage('error', 'Something went wrong. Please try again later.');
    }
  };

  // const handleSubmit = async (e) => {
  //   e.preventDefault();

  //   // Check if all fields are filled
  //   if (username.trim() === '' || password.trim() === '' || email.trim() === '') {
  //     displayMessage('error', 'All fields are required.');
  //     return;
  //   }

  //   // Check if email is valid
  //   if (email && email.trim() !== '' && !isValidEmail(email)) {
  //       displayMessage('error', 'Invalid email format');
  //       return;
  //   }

  //   // Send request to backend
  //   try {
  //     // Initial code:                  fetch('http://localhost:5000/api/signup')
  //     // Change to use AWS Backend URL: fetch(`${config.apiURL}/signup`)      
  //     // note: backticks to use template strings, not apostrophes (regular strings) here
  //     const response = await fetch(`${config.apiURL}/signup`, {
  //         method: 'POST',
  //         headers: {
  //             'Content-Type': 'application/json'
  //         },
  //         body: JSON.stringify({ username, password, email })
  //     });
    
  //     // Check if response is ok
  //     if (!response.ok) {
  //       const data = await response.json();
  //       displayMessage('error', data.error || 'Signup failed.');
  //       return;
  //     }

  //     // If response is ok, display success message
  //     displayMessage('success', 'Signup successful!');
  //     console.log('success')

  //     // Response error
  //   } catch (error) {
  //     displayMessage('error', 'Something went wrong. Please try again later.');
  //   }
  // };

  // Function to display messages
  const displayMessage = (type, content) => {
    setMessage({ type, content });
    setTimeout(() => setMessage({ type: '', content: '' }), 50000); // Clear the message after 50 seconds
  };

  // Function to check if email is valid
  const isValidEmail = (email) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
  };

  return (
    <div className="login-container">
      <h1 className="page-title">Welcome to The Dupe Machine</h1>
      <h2 className="login-title">Sign Up</h2>

      {/* Display message if it exists */}
      {message.content && (
                <div className={`message-box ${message.type}`}>
                    <p>{message.content}</p>
                </div>
            )}

      <form className="login-box">
        <input type="text" 
              placeholder="Username" 
              className="input-field" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}/>
        <input type="email" 
              placeholder="Email" 
              className="input-field" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}/>
        <input type="password" 
              placeholder="Password" 
              className="input-field" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}/>
        <button className="login-button"onClick={handleSubmit}>Sign Up</button>
      </form>
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