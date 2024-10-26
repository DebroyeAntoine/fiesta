import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GameTable from '../components/GameTable';

const GamePage: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    if (!gameId ) {
      console.error("Invalid parameters, redirecting to home");
      navigate("/");
    } else {
      console.log("gameId:", gameId);
    }
  }, [gameId, navigate]);

  if (!gameId) {
    return null;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900">
      {/* Titre stylisé */}
      <h1 className="text-6xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 drop-shadow-lg my-10">
        Fiesta de Los Muertos
      </h1>

      {/* Passe les props à GameTable */}
      <GameTable gameId={gameId} />
    </div>
  );
};

export default GamePage;

