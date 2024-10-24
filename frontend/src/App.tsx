import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './pages/Home'; // Page d'accueil
import RegisterPage from './pages/RegisterPage'; // Page d'inscription
import LoginPage from './pages/LoginPage'; // Page d'inscription
import GamePage from './pages/GamePage'; // Page d'inscription

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/game/:gameId/player/:playerId/round/:roundId" element={<GamePage />} />

      {/* Ajoute d'autres routes ici */}
      </Routes>
    </Router>
  );
};

export default App;

