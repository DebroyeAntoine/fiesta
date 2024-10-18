import React, { useState, useEffect, useCallback } from 'react';
import PlayerAvatar from './PlayerAvatar';
import SkullCard from './SkullCard';

interface GameTableProps {
  gameId: string;
  playerId: string;
  roundId: string;
}

const GameTable : React.FC<GameTableProps> = ({gameId, playerId, roundId}) => {
  const [word, setWord] = useState('');  // Le mot ou l'indice affiché sur la carte tête de mort
  const [players, setPlayers] = useState([
    { id: 1, name: 'Player 1', hasSubmitted: false },
    { id: 2, name: 'Player 2', hasSubmitted: false },
    { id: 3, name: 'Player 3', hasSubmitted: false },
    { id: 4, name: 'Player 4', hasSubmitted: false },
  ]);
  const [submittedPlayers, setSubmittedPlayers] = useState<number[]>([]);  // IDs des joueurs ayant soumis leur mot

  const handleValidate = async () => {
    try {
      const token = localStorage.getItem('token');  // Assure-toi que tu récupères correctement le token
      /* TODO change with backend logical */
      const roundId = 'id-du-round';  // Remplace par la logique pour obtenir le roundId
      const playerId = 990;  // Remplace par l'ID du joueur actuel (peut être stocké dans le contexte de l'utilisateur)
  
      const response = await fetch(`/round/${roundId}/player/${playerId}/submit_word`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ word }),
      });
  
      if (response.ok) {
        // Si le mot a bien été soumis, ajoute l'ID du joueur dans la liste
        setSubmittedPlayers(prev => [...prev, playerId]);
      }
    } catch (error) {
      console.error('Error submitting word:', error);
    }
  };
  
  const goToNextRound = useCallback(async () => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`/round/${roundId}/next`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        console.log('Passage au round suivant réussi !');
        // Mettre à jour l'état du round si nécessaire
      } else {
        console.error('Erreur lors du passage au round suivant.');
      }
    } catch (error) {
      console.error('Error advancing to next round:', error);
    }
  }, [roundId]);
 
    useEffect(() => {
    // Vérifie si tous les joueurs ont validé leur mot
    if (submittedPlayers.length === players.length) {
      console.log('Tous les joueurs ont soumis leur mot ! Passons au round suivant.');
      goToNextRound();  // Appelle la fonction pour avancer au round suivant
    }
  }, [submittedPlayers, players, goToNextRound]);  // Le hook se déclenchera à chaque fois que submittedPlayers change


  return (
    <div className="game-table relative w-full h-screen flex justify-center items-center">
      <div className="center-skull-card absolute bottom-10">
        <SkullCard word={word} setWord={setWord} handleValidate={handleValidate} />
      </div>

      <div className="player-circle grid grid-cols-4 gap-4">
        {players.map((player) => (
           <PlayerAvatar
             key={player.id}
             player={player}
             hasSubmitted={submittedPlayers.includes(player.id)}  // Check si le joueur a soumis son mot
           />
        ))}
      </div>
    </div>
  );
};

export default GameTable;

