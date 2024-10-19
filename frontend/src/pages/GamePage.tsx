import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GameTable from '../components/GameTable';

const GamePage: React.FC = () => {
  const { gameId, playerId, roundId } = useParams<{ gameId: string, playerId: string, roundId: string}>();  // Récupère les paramètres de l'URL
  const navigate = useNavigate();

  // Optionnel : Si tu veux tester et être sûr de recevoir les bons paramètres
  useEffect(() => {
    if (!gameId || !playerId || !roundId) {
      navigate("/");  // Rediriger vers la page d'accueil ou une autre page
    }
    console.log("gameId:", gameId, "playerId:", playerId, "roundId:", roundId);
  }, [gameId, playerId, roundId, navigate]);

  if (!gameId || !playerId || !roundId) {
    return null;
  }
  return (
    <div className="game-page">
      {/* Passe les props à GameTable */}
      <GameTable gameId={gameId} playerId={playerId} roundId={roundId} />
    </div>
  );
};

export default GamePage;

