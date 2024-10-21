import React, { useState, useEffect, useCallback } from 'react';
import PlayerAvatar from './PlayerAvatar';
import SkullCard from './SkullCard';
import InitialWord from './InitialWord';
import { io } from 'socket.io-client';

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
    const socket = io('http://localhost:5000', {
      transports: ['websocket'], // Utilise uniquement WebSocket
    });
    // Écoute les événements WebSocket pour les nouveaux joueurs
    socket.on('update_player_list', (data) => {
    // Le 'data' contient la liste des joueurs, on va la mettre à jour dans l'état
      setPlayers(data.players); // Met à jour directement avec la nouvelle liste de joueurs
    });// Écoute les événements lorsque des joueurs quittent
    socket.on('player_left', (playerData: { id: number }) => {
      setPlayers((prevPlayers) => prevPlayers.filter((player) => player.id !== playerData.id));
    });

    // Récupérer la liste des joueurs à l'initialisation
    const fetchPlayers = async () => {
      const token = localStorage.getItem('token');
      const response = await fetch(`/game/${gameId}/players`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      setPlayers(data.players);
      setLoading(false);
    };

    fetchPlayers();

    return () => {
      socket.off('player_update');
      socket.off('player_left');
    };
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
    if (submittedPlayers.length === players.length && players.length > 0) {
      console.log('Tous les joueurs ont soumis leur mot ! Passons au round suivant.');
      goToNextRound(); // Appelle la fonction pour avancer au round suivant
    }
  }, [submittedPlayers, players, goToNextRound]); // Le hook se déclenchera à chaque fois que submittedPlayers change

  if (loading) {
    return <div>Chargement des joueurs...</div>; // Vous pouvez remplacer ceci par un spinner ou un autre composant de chargement
  }

  return (
    <div className="game-table relative w-full min-h-screen flex flex-col justify-start items-center"> {/* Ajout de pt-20 pour espacer du haut */}
      <InitialWord gameId={gameId} />

      {/* Section des avatars des joueurs */}
      <div className="player-row flex justify-center items-center gap-6 flex-wrap mb-4 mt-4"> {/* Réduction des marges en haut et en bas */}
        {Array.isArray(players) && players.length > 0 ? (
          players.map((player) => (
            <div key={player.id} className="player-container flex flex-col items-center">
              {player.id === playerId ? (
                // Ne pas afficher l'avatar du joueur courant ici
                <></>
              ) : (
                <PlayerAvatar
                  player={{ id: player.id, username: player.username }}
                  hasSubmitted={submittedPlayers.includes(player.id)}
                />
              )}
            </div>
          ))
        ) : (
          <p>No players available</p> // Fallback si aucun joueur n'est disponible
        )}
      </div>

      {/* Section de la SkullCard du joueur courant */}
      {players.some(player => player.id === playerId) && (
        <div className="skull-card mt-6"> {/* Réduction de la marge supérieure */}
          <SkullCard word={word} setWord={setWord} handleValidate={handleValidate} />
        </div>
      )}
    </div>
  );
};

export default GameTable;

