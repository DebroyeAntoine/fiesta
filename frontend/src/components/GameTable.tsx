import React, { useState, useEffect } from 'react'; // Suppression de 'useCallback' car non utilisé
import PlayerAvatar from './PlayerAvatar';
import SkullCardInput from './SkullCardInput';
import InitialWord from './InitialWord';
import { io } from 'socket.io-client';

interface GameTableProps {
    gameId: string;
    playerId: number;
    roundId: string;
}

interface Player {
    id: number; // Assumons que l'ID soit de type number
    username: string;
    word_submitted?: boolean; // Ajout de l'état de soumission
}

const GameTable: React.FC<GameTableProps> = ({ gameId, playerId, roundId }) => {
    const [word, setWord] = useState(''); // Le mot ou l'indice affiché sur la carte tête de mort
    const [players, setPlayers] = useState<Player[]>([]);
    const [submittedPlayers, setSubmittedPlayers] = useState<number[]>([]); // IDs des joueurs ayant soumis leur mot
    const [loading, setLoading] = useState(true); // État de chargement
    const [newRound, setNewRound] = useState(false); // Nouvel état pour suivre si un nouveau round a été déclenché

    const handleNewRound = () => {
        setNewRound(prev => !prev); // Changez l'état pour forcer le composant à se mettre à jour
        setWord(prev => '');
        setSubmittedPlayers(prev => [])
    };

    const handleValidate = async () => {
        try {
            const token = localStorage.getItem('token'); // Assure-toi que tu récupères correctement le token

            const response = await fetch(`/game/submit_word`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    word: word,
                    round_id: roundId,
                    game_id: gameId
                }),
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

            // Mettre à jour la liste des joueurs ayant soumis un mot
            const submittedIds = data.players
                .filter((player: Player) => player.word_submitted) // Filtrer ceux qui ont soumis un mot
                .map((player: Player) => player.id); // Récupérer les IDs des joueurs qui ont soumis

            setSubmittedPlayers(submittedIds);
        });

        // Écoute les événements lorsque des joueurs quittent
        socket.on('player_left', (playerData: { id: number }) => {
            setPlayers((prevPlayers) => prevPlayers.filter((player) => player.id !== playerData.id));
        });

        socket.on('new_round', (data) => {
            console.log(`New round started: ${data.round_id}`);
            handleNewRound();
        });

        socket.on('word_submitted', (data) => {
            console.log(`Player ${data.player_id} submitted the word: ${data.word}`);
            // Mettez à jour l'interface utilisateur ici
            setSubmittedPlayers((prev) => [...prev, data.player_id]);
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

            // Mettre à jour la liste des joueurs ayant soumis un mot
            const submittedIds = data.players
                .filter((player: Player) => player.word_submitted) // Filtrer ceux qui ont soumis un mot
                .map((player: Player) => player.id); // Récupérer les IDs des joueurs qui ont soumis

            setSubmittedPlayers(submittedIds);
            setLoading(false);
        };

        fetchPlayers();

        return () => {
            socket.off('player_update');
            socket.off('player_left');
            socket.off('word_submitted');
            socket.off('new_round');
        };
    }, [gameId]);

    if (loading) {
        return <div>Chargement des joueurs...</div>; // Vous pouvez remplacer ceci par un spinner ou un autre composant de chargement
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
                                // Ne pas afficher l'avatar du joueur courant ici
                                <></>
                            ) : (
                                <PlayerAvatar
                                    player={{ id: player.id, username: player.username }}
                                    hasSubmitted={submittedPlayers.includes(player.id)} // Passer l'état de soumission
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
                <div className="skull-card mt-6">
                    <SkullCardInput word={word} setWord={setWord} handleValidate={handleValidate} />
                </div>
            )}
        </div>
    );
};

export default GameTable;

