
import{ BrowserRouter, Routes, Route} from 'react-router-dom';
import loginPage from "./components/loginPage";
import ImageDescription from "./components/ImageDescription";
import './App.css';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<loginPage />} />
        <Route path="/description" element={<ImageDescription />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
