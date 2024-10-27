import React, { useState, useEffect } from 'react';
import PlayerAvatar from './PlayerAvatar';
import SkullCardInput from './SkullCardInput';
import InitialWord from './InitialWord';
import { io } from 'socket.io-client';
import { useNavigate } from 'react-router-dom';

interface GameTableProps {
    gameId: string;
}

interface Player {
    id: number;
    username: string;
    word_submitted?: boolean;
}

const GameTable: React.FC<GameTableProps> = ({ gameId}) => {
    const [playerId, setPlayerId] = useState<number>(0)
    const [word, setWord] = useState('');
    const [players, setPlayers] = useState<Player[]>([]);
    const [submittedPlayers, setSubmittedPlayers] = useState<number[]>([]);
    const [loading, setLoading] = useState(true);
    const [newRound, setNewRound] = useState(false);
    const [roundId, setRoundId] = useState<number>(0);
    const navigate = useNavigate()

    const handleNewRound = (round_id: number) => {
        setRoundId(round_id);
        setNewRound(prev => !prev);
        setWord('');
        setSubmittedPlayers([]);
    };

    const handleValidate = async () => {
        if (playerId === null) return;
        try {
            const token = localStorage.getItem('token');

            const response = await fetch(`/game/submit_word`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    word: word,
                    round_id: roundId,
                    game_id: gameId,
                }),
            });

            if (response.ok) {
                setSubmittedPlayers(prev => [...prev, playerId as number]);
            }
        } catch (error) {
            console.error('Error submitting word:', error);
        }
    };

    useEffect(() => {
        const fetchGameInfo = async () => {
            const token = localStorage.getItem('token');
            const response = await fetch(`/game/${gameId}/get_game_infos`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setPlayers(data.players);
                setRoundId(data.round_id);
                setPlayerId(data.player_id);
                setLoading(false);
            } else {
                console.error('Failed to fetch game info');
                setLoading(false);
            }
        };

        fetchGameInfo();

        // Clean-up socket listeners
        const socket = io('http://localhost:5000', {
            transports: ['websocket'],
        });

    socket.on('update_player_list', (data) => {
            setPlayers(data.players);

            const submittedIds = data.players
                .filter((player: Player) => player.word_submitted)
                .map((player: Player) => player.id);

            setSubmittedPlayers(submittedIds);
        });

        socket.on('player_left', (playerData: { id: number }) => {
            setPlayers(prevPlayers => prevPlayers.filter(player => player.id !== playerData.id));
        });

        socket.on('new_round', (data : { round_id: number}) => {
            console.log(`New round started: ${data.round_id}`);
            handleNewRound(Number(data.round_id));
        });

        socket.on('word_submitted', (data) => {
            console.log(`Player ${data.player_id} submitted the word: ${data.word}`);
            setSubmittedPlayers(prev => [...prev, data.player_id]);
        });

        socket.on('game_over', (data:  { initial_words: string[]; end_words: string[] }) => {
            console.log(`datas: ${data.initial_words}`);
            navigate(`/gameOver/${gameId}`, { state: { skullWords: data.end_words, characters: data.initial_words } });
        });

        return () => {
            socket.off('update_player_list');
            socket.off('player_left');
            socket.off('word_submitted');
            socket.off('new_round');
            socket.off('game_over');
        };}, [gameId, navigate]);

    if (loading) {
        return <div>Chargement des joueurs...</div>;
    }

    return (
        <div className="game-table relative w-full min-h-screen flex flex-col justify-start items-center">
            <InitialWord gameId={gameId} refreshKey={newRound} />
            {/* Section des avatars des joueurs */}
            <div className="player-row flex justify-center items-center gap-6 flex-wrap mb-4 mt-4">
                {Array.isArray(players) && players.length > 0 ? (
                    players.map((player) => (
                        <div key={player.id} className="player-container flex flex-col items-center">
                            {player.id === playerId ? (
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
                    <p>No players available</p>
                )}
            </div>
            {/* Section de la SkullCard du joueur courant */}
            {players.some(player => player.id === playerId) && (
                <div className="skull-card mt-6">
                    <SkullCardInput word={word} setWord={setWord} handleValidate={handleValidate} />
                </div>
            )}
        </div>
    );
};

export default GameTable;

