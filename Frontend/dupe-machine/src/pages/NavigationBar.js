import React from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import "../styling/NavigationBar.css";

function NavigationBar()  {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="navbar">
      <div className = "link-container">
      <span 
        className={`nav-link ${location.pathname}`} 
        onClick={() => navigate('/')}
      >
        Login 
      </span>
      <span 
        className={`nav-link ${location.pathname}`} 
        onClick={() => navigate('/main')}
      >
        Main Page
      </span>
      <span 
        className={`nav-link ${location.pathname}`} 
        onClick={() => navigate('/profile')}
      >
        Profile
      </span>
      </div>
    </div>
  );
};

export default NavigationBar;