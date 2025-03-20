import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from '../AuthContext';
import "../styling/LoginPage.css";

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState({ type: '', content: '' }); // State to manage the message
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchCookie();
  }, []);

  //function for cookies
  const fetchCookie = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/cookie', {
            method: 'GET',
            credentials: 'include'  // Ensure cookies are sent with the request
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Logged-in user:', data.username);
            setUsername(data.username);  // Set username in state
            login(data.username); // Update authentication state
            console.log('isAuthenticated set to true'); // DEBUG CODE Log the state change
        } else {
            console.log('No cookie found');
        }
    } catch (error) {
        console.error('Error fetching cookie:', error);
    }
  };

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
          credentials: 'include' 
      });
      if (response.ok) {
        setMessage({ type: 'success', content: 'Authentication successful' });
        console.log('success')
        fetchCookie();
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
      <h1 className="page-title">Welcome to The Dupe Machine</h1>
      <h2 className="login-title">Login</h2>
      {/* Display message if it exists */}
      {message.content && (
                <div className={`message-box ${message.type}`}>
                    <p>{message.content}</p>
                </div>
            )}
      <form className="login-box">
        <input type="text" placeholder="Username" className="input-field" 
          value={username}
          onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" className="input-field" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="login-button" onClick={handleSubmit}>Login</button>
      </form>
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
