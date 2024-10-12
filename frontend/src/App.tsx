import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './pages/Home'; // Page d'accueil
import RegisterPage from './pages/RegisterPage'; // Page d'inscription

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<RegisterPage />} />
        {/* Ajoute d'autres routes ici */}
      </Routes>
    </Router>
  );
};

export default App;

