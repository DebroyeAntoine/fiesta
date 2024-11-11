import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import { SocketProvider } from './context/SocketContext';
import Home from './pages/Home'; // Page d'accueil
import RegisterPage from './pages/RegisterPage'; // Page d'inscription
import LoginPage from './pages/LoginPage'; // Page d'inscription
import GamePage from './pages/GamePage'; // Page d'inscription
import GameOverPage from './pages/GameOver';
import GameListPage from './pages/GameListPage';

const App = () => {
  return (
    <SocketProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/game/:gameId" element={<GamePage />} />
          <Route path="/gameOver/:gameId" element={<GameOverPage />} />
          <Route path="/gameList" element={<GameListPage />} />
        {/* Ajoute d'autres routes ici */}
        </Routes>
      </Router>
    </SocketProvider>
  );
};

export default App;

