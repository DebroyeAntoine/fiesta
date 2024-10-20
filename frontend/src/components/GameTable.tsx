import React, { useState, useEffect, useCallback } from 'react';
import PlayerAvatar from './PlayerAvatar';
import SkullCard from './SkullCard';

interface GameTableProps {
  gameId: string;
  playerId: number;
  roundId: string;
}

interface Player {
  id: number;  // Assumons que l'ID soit de type string
  username: string;
}

const GameTable : React.FC<GameTableProps> = ({gameId, playerId, roundId}) => {
  const [word, setWord] = useState('');  // Le mot ou l'indice affiché sur la carte tête de mort
  const [players, setPlayers] = useState<Player[]>([]);
  const [submittedPlayers, setSubmittedPlayers] = useState<number[]>([]);  // IDs des joueurs ayant soumis leur mot
  const [loading, setLoading] = useState(true); // État de chargement

  const handleValidate = async () => {
    try {
      const token = localStorage.getItem('token');  // Assure-toi que tu récupères correctement le token
      /* TODO change with backend logical */
  
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

  useEffect(() => {
    const fetchPlayers = async () => {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch(`/game/${gameId}/players`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPlayers(data.players);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des joueurs:', error);
      } finally {
        setLoading(false); // Arrête le chargement, que la requête réussisse ou échoue
      }
    };

    fetchPlayers();
  }, [gameId]);
  
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
    if (submittedPlayers.length === players.length && players.length >0) {
      console.log('Tous les joueurs ont soumis leur mot ! Passons au round suivant.');
      goToNextRound();  // Appelle la fonction pour avancer au round suivant
    }
  }, [submittedPlayers, players, goToNextRound]);  // Le hook se déclenchera à chaque fois que submittedPlayers change
  if (loading) {
    return <div>Chargement des joueurs...</div>; // Vous pouvez remplacer ceci par un spinner ou un autre composant de chargement
  }
  console.log(typeof(playerId));
  return (
    <div className="game-table relative w-full h-screen flex justify-center items-center">
      <div className="player-circle grid grid-cols-1 gap-4 w-full"> {/* Affichez 1 joueur par ligne */}
        {Array.isArray(players) && players.length > 0 ? (
          players.map((player) => {
            console.log(typeof(player.id))
            return (
              <div key={player.id} className="player-container flex flex-col items-center">
                {/* Si c'est le joueur courant, affiche sa SkullCard */}
                {player.id === playerId ? (
                  <SkullCard word={word} setWord={setWord} handleValidate={handleValidate} />
                ) : (
                  <PlayerAvatar
                    player={{ id: player.id, username: player.username }}
                    hasSubmitted={submittedPlayers.includes(player.id)}
                  />
                )}
              </div>
            );
          })
        ) : (
          <p>No players available</p>  // Fallback si aucun joueur n'est disponible
        )}
      </div>
    </div>
  );
};
export default GameTable;

