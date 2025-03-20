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

  const logout = () => {
    setIsAuthenticated(false);
    setUsername('');
    console.log('User logged out. isAuthenticated:', false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, username, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);