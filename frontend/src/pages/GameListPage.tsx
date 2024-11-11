// src/pages/GameList.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSocket } from '../context/SocketContext';

interface Game {
  id: number;
  name: string;
  playerCount: number;
  maxPlayers: number;
  status: string;
}

const GameListPage: React.FC = () => {
  const socket = useSocket();
  const navigate = useNavigate();
  const [games, setGames] = useState<Game[]>([]);
  const [creatingGame, setCreatingGame] = useState(false);  // Indicate if game creation is in progress
  const [newGameId, setNewGameId] = useState<number | null>(null);  // Store the game ID for redirection
  const [gameCreated, setGameCreated] = useState(false);  // Flag to track if the game was created

  useEffect(() => {
    const fetch_games = async () => {
      try {
          const token = localStorage.getItem('token');
          const response = await fetch('game/get_games', {
              method: 'GET',
              headers: {
                  'Content-Type': 'application/json',
                  Authorization: `Bearer ${token}`,
              },
          });
          if (response.ok) {
              const data = await response.json();
              setGames(data.games);
          }
      } catch (error) {
            console.error('Error fetching games', error);
      }
    };

    fetch_games();

    socket.on('games_list', (data) => setGames(data.games));

    socket.on('game_created', (data) => {
      if (data.success) {
        setGames((prevGames) => [
          ...prevGames,
          { id: data.game_id, name: 'New Game', playerCount: 1, maxPlayers: 4, status: 'waiting' },
        ]);

        if (creatingGame) {
          setGameCreated(true);
          setNewGameId(data.game_id); // Save ID
        }
      }
    });

    return () => {
      socket.off('games_list');
      socket.off('game_created');
    };
  }, [socket, creatingGame]);

  useEffect(() => {
    if (gameCreated && newGameId !== null) {
      navigate(`/game/${newGameId}/lobby`);
      setGameCreated(false);
    }
  }, [gameCreated, newGameId, navigate]);

  const handleJoinGame = (gameId: number) => {
    socket.emit('join_game', { game_id: gameId });
    navigate(`/game/${gameId}/lobby`);
  };

  const handleCreateGame = () => {
    setCreatingGame(true);
    socket.emit('create_game', { token: localStorage.getItem('token') }, (response: any) => {
      if (response.success) {
      }
    });
  };

  return (
    <div className="game-list-page min-h-screen bg-yellow-50 p-6 flex flex-col items-center">
      <h1 className="text-3xl text-orange-600 font-bold mb-6">🎉 Select or Create a Game 🎉</h1>
      <div className="w-full max-w-2xl space-y-4">
        <button
          className="create-game-button bg-purple-500 text-white py-2 px-6 rounded-full w-full hover:bg-purple-600 transition duration-300"
          onClick={handleCreateGame}
        >
          Create New Game
        </button>
        <div className="game-list space-y-2">
          {games.length > 0 ? (
            games.map((game) => (
              <div
                key={game.id}
                className="game-item p-4 bg-white rounded-lg shadow-md flex justify-between items-center hover:bg-yellow-100 transition"
              >
                <div>
                  <h2 className="text-lg font-semibold text-orange-700">{game.name}</h2>
                  <p className="text-gray-500">{game.playerCount}/{game.maxPlayers} players</p>
                </div>
                <button
                  className="join-game-button bg-green-500 text-white py-1 px-4 rounded-full hover:bg-green-600 transition"
                  onClick={() => handleJoinGame(game.id)}
                  disabled={game.playerCount >= game.maxPlayers}
                >
                  Join
                </button>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No games available. Create one to start playing!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameListPage;

