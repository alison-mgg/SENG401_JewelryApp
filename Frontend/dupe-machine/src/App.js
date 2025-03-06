import TempLoginPage from './pages/TempLoginPage';
import MainPage from './pages/MainPage';
import SignupPage from './pages/SignupPage';
import ProfilePage from './pages/ProfilePage';
import{ BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<TempLoginPage />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
