import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GameTable from '../components/GameTable';

const GamePage: React.FC = () => {
  // Récupère les paramètres de l'URL
  const { gameId, playerId, roundId } = useParams<{ gameId: string, playerId: string, roundId: string }>();
  const navigate = useNavigate();
  const playerIdNumber = Number(playerId);

  // Vérification des paramètres et redirection si invalides
  useEffect(() => {
    if (!gameId || isNaN(playerIdNumber) || !roundId) {
      console.error("Invalid parameters, redirecting to home");
      navigate("/"); // Rediriger vers la page d'accueil si les paramètres sont manquants ou invalides
    } else {
      console.log("gameId:", gameId, "playerId:", playerIdNumber, "roundId:", roundId);
    }
  }, [gameId, playerIdNumber, roundId, navigate]); // Ajout de playerIdNumber dans les dépendances

  // Vérification supplémentaire avant de rendre le composant
  if (!gameId || !playerId || !roundId || isNaN(playerIdNumber)) {
    return null; // Si les paramètres sont invalides, on retourne null (ou tu pourrais rediriger vers une erreur)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900">
      {/* Titre stylisé */}
      <h1 className="text-6xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 drop-shadow-lg my-10">
        Fiesta de Los Muertos
      </h1>

      {/* Passe les props à GameTable */}
      <GameTable gameId={gameId} playerId={playerIdNumber} roundId={roundId} />
    </div>
  );
};

export default GamePage;

