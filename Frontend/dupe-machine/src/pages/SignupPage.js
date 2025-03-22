import React, { useState }from "react";
import { Link, useNavigate  } from "react-router-dom";
import "../styling/SignupPage.css";

function SignupPage() {

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' });
  const navigate = useNavigate();

 // Function to handle the form submission
const handleSubmit = async (e) => {
  e.preventDefault();  // Prevents the default form submission behavior
  
  // Check if any required fields are empty (username, password, or email)
  if (username.trim() === '' || password.trim() === '' || email.trim() === '') {
    displayMessage('error', 'All fields are required.');  // Display error message
    return;  // Stop the function if validation fails
  }

  // Validate email format using regex
  if (email && email.trim() !== '' && !isValidEmail(email)) {
    displayMessage('error', 'Invalid email format');  // Display error message if email format is invalid
    return;  // Stop the function if email is invalid
  }

  try {
    // Send a POST request to the backend API for signup
    const response = await fetch('http://localhost:5000/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password, email }),  // Send username, password, and email in the request body
    });

    // Check if the response from the server is successful
    if (!response.ok) {
      const data = await response.json();  // Parse error message from response
      displayMessage('error', data.error || 'Signup failed.');  // Display error message
      return;  // Stop the function if signup failed
    }

    // Display success message after successful signup
    displayMessage('success', 'Signup successful! Redirecting to login...');
    
    // Redirect to the login page after 2 seconds
    setTimeout(() => {
      navigate('/');  // Navigate to login page
    }, 2000); // Delay of 2 seconds before redirection

  } catch (error) {
    // Catch any errors that occur during the signup process and display an error message
    displayMessage('error', 'Something went wrong. Please try again later.');
  }
};

// Function to display messages with a specific type (success or error)
const displayMessage = (type, content) => {
  setMessage({ type, content });  // Set the message state with the type and content
  setTimeout(() => setMessage({ type: '', content: '' }), 50000);  // Clear the message after 50 seconds
};

// Function to validate email format using a regex pattern
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;  // Regex for valid email format
  return emailRegex.test(email);  // Return true if email matches the regex, otherwise false
};



  return (
    <div className="login-container">
        <div className="loginArea">
        <div className="login-box">
      <h1 className="page-title">Welcome to The Dupe Machine</h1>
      <h2 className="login-title">Sign Up</h2>

      {/* Display message if it exists */}
      {message.content && (
                <div className={`message-box ${message.type}`}>
                    <p>{message.content}</p>
                </div>
            )}

<form className="login-form">
      <div className="input-group">
        <input type="text" 
              placeholder="Username" 
              className="input-field" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}/>
              </div>
              <div className="input-group">
        <input type="email" 
              placeholder="Email" 
              className="input-field" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}/>
              </div>
              <div className="input-group">
        <input type="password" 
              placeholder="Password" 
              className="input-field" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}/>
              </div>
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
    <div className="loginImage"></div>
      </div>
    </div>
  );
}

export default SignupPage;