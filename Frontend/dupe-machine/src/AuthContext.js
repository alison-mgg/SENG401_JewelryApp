
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  const login = (username) => {
    setIsAuthenticated(true);
    setUsername(username);
    console.log('User logged in. isAuthenticated:', true);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, username, login }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);