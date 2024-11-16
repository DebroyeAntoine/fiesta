// src/pages/Lobby.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { useSocket } from '../context/SocketContext';
import PlayerList from '../components/PlayerList';
import ReadyButton from '../components/ReadyButton';
import StartGameButton from '../components/StartGameButton';
import GameStatus from '../components/GameStatus';

const Lobby: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const socket = useSocket();
  const [players, setPlayers] = useState([]);
  const [isOwner, setIsOwner] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const navigate = useNavigate();



  useEffect(() => {

    const fetch_games = async () => {
       try {
           const token = localStorage.getItem('token');
           const response = await fetch(`/game/${gameId}/get_lobby`, {
               method: 'GET',
               headers: {
                   'Content-Type': 'application/json',
                   Authorization: `Bearer ${token}`,
               },
           });
           if (response.ok) {
               const data = await response.json();
               setPlayers(data.players)
               setIsOwner(data.isOwner);
           }
       } catch (error) {
             console.error('Error fetching games', error);
       }
     };

     fetch_games();
    //socket.emit('join_game', { game_id: gameId });
    socket.on('player_joined', (data) => {
      //  if (data.player) {
        //    setPlayers(data.player);
        //}
        console.log(data.player);
    });
    socket.on('players_update', (data) => {setPlayers(data);});
    socket.on('changing_ownership', () =>  {console.log("coucou");fetch_games();});
    socket.on('player_left', data => setPlayers(data.players));
    socket.on('player_ready_update', data => setPlayers(data.players));
    socket.on('game_started', () => navigate(`/game/${gameId}`));
    socket.on('game_info', data => setIsOwner(data.owner_id === socket.id));

    return () => {
      socket.emit('leave_game', { game_id: gameId, player_token: localStorage.getItem('token')});
      socket.off('player_joined');
      socket.off('player_left');
      socket.off('players_update');
      socket.off('game_started');
      socket.off('game_info');
    };
  }, [socket, gameId, navigate]);

  const handleReady = () => {
    socket.emit('player_ready', { game_id: gameId });
    setIsReady(!isReady);
  };

  const handleStartGame = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`/game/${gameId}/start`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
    });
    if (!response.ok) {
        console.error("error when creating game");
    }
  };

  return (
    <div className="lobby-page bg-yellow-100 min-h-screen p-6 flex flex-col items-center">
      <h1 className="text-3xl text-orange-600 font-bold mb-4">
        🎉 Lobby - Game {gameId} 🎉
      </h1>
      {/*<GameStatus players={players} isOwner={isOwner} />*/}
      <PlayerList players={players} />
      {/*<{ReadyButton isReady={isReady} onClick={handleReady} />*/}
      {isOwner && <StartGameButton onClick={handleStartGame} />}
    </div>
  );
};

export default Lobby;

