import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';
import SignupPage from './pages/SignupPage';
import ProfilePage from './pages/ProfilePage';
import Upload from './pages/UploadImageText';
import React, { createContext, useContext, useState } from 'react';
import{ BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';

const AuthContext = createContext();
export const useAuthContext = () => useContext(AuthContext);
export const AuthProvider = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);

  return(
    <AuthContext.Provider value={{ authenticated, setAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/UploadImageText" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
