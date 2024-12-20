import React, { useState, useEffect } from "react";
import PlayerAvatar from "./PlayerAvatar";
import SkullCardInput from "./SkullCardInput";
import InitialWord from "./InitialWord";
import ConstraintCard from "./Constraint";
import { useSocket } from "../context/SocketContext";
import { useNavigate } from "react-router-dom";

interface GameTableProps {
    gameId: string;
}

interface Player {
    id: number;
    username: string;
    word_submitted?: boolean;
}

const GameTable: React.FC<GameTableProps> = ({ gameId }) => {
    const [playerId, setPlayerId] = useState<number>(0);
    const [word, setWord] = useState<string>("");
    const [constraints, setConstraints] = useState<string[]>([]);
    const [players, setPlayers] = useState<Player[]>([]);
    const [submittedPlayers, setSubmittedPlayers] = useState<number[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [newRound, setNewRound] = useState<boolean>(false);
    const [roundId, setRoundId] = useState<number>(0);
    const navigate = useNavigate();
    const socket = useSocket();

    const handleNewRound = (round_id: number) => {
        setRoundId(round_id);
        setNewRound((prev) => !prev);
        setWord("");
        setSubmittedPlayers([]);
    };

    const handleValidate = async () => {
        if (playerId === null) return;
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`/game_api/game/submit_word`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    word: word,
                    round_id: roundId,
                    game_id: gameId,
                }),
            });

            if (response.ok) {
                setSubmittedPlayers((prev) => [...prev, playerId]);
            }
        } catch (error) {
            console.error("Error submitting word:", error);
        }
    };

    useEffect(() => {
        const fetchGameInfo = async () => {
            const token = localStorage.getItem("token");
            const response = await fetch(
                `/game_api/game/${gameId}/get_game_infos`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.ok) {
                const data = await response.json();
                setPlayers(data.players);
                setRoundId(data.round_id);
                setPlayerId(data.player_id);
                setConstraints(data.constraints || []);
                setLoading(false);
            } else {
                console.error("Failed to fetch game info");
                setLoading(false);
            }
        };

        fetchGameInfo();

        // Clean-up socket listeners
        socket.on("update_player_list", (data) => {
            setPlayers(data.players);

            const submittedIds = data.players
                .filter((player: Player) => player.word_submitted)
                .map((player: Player) => player.id);

            setSubmittedPlayers(submittedIds);
        });

        socket.on("player_left", (playerData: { id: number }) => {
            setPlayers((prevPlayers) =>
                prevPlayers.filter((player) => player.id !== playerData.id)
            );
        });

        socket.on("new_round", (data: { round_id: number }) => {
            console.log(`New round started: ${data.round_id}`);
            handleNewRound(Number(data.round_id));
        });

        socket.on("word_submitted", (data) => {
            console.log(
                `Player ${data.player_id} submitted the word: ${data.word}`
            );
            setSubmittedPlayers((prev) => [...prev, data.player_id]);
        });

        socket.on(
            "game_over",
            (data: { initial_words: string[]; end_words: string[] }) => {
                console.log(`datas: ${data.initial_words}`);
                navigate(`/gameOver/${gameId}`, {
                    state: {
                        skullWords: data.end_words,
                        characters: data.initial_words,
                        game_id: gameId,
                    },
                });
            }
        );

        return () => {
            socket.off("update_player_list");
            socket.off("player_left");
            socket.off("word_submitted");
            socket.off("new_round");
            socket.off("game_over");
        };
    }, [gameId, navigate, socket]);

    if (loading) {
        return <div>Chargement des joueurs...</div>;
    }

    return (
        <div className="game-table relative w-full min-h-screen flex flex-col justify-start items-center">
            <div className="absolute top-4 left-4 flex flex-col gap-4">
                {/* Composant Initial Word */}
                <InitialWord gameId={gameId} refreshKey={newRound} />

                {/* Liste des contraintes */}
                {constraints.length > 0 && (
                    <div className="constraints-list p-4 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg shadow-lg border-4 border-indigo-400">
                        <h2 className="text-2xl font-bold text-white mb-3 drop-shadow-lg">
                            Contraintes
                        </h2>
                        <ul className="space-y-2">
                            {constraints.map((constraint, index) => (
                                <li
                                    key={index}
                                    className="bg-white text-indigo-800 px-4 py-2 rounded-lg shadow hover:bg-indigo-200 transition duration-300 ease-in-out"
                                >
                                    {constraint}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Section des avatars des joueurs */}
            <div className="player-row flex justify-center items-center gap-6 flex-wrap mb-4 mt-4">
                {Array.isArray(players) && players.length > 0 ? (
                    players.map((player) => (
                        <div
                            key={player.id}
                            className="player-container flex flex-col items-center"
                        >
                            {/* N'affiche pas l'avatar du joueur courant */}
                            {player.id !== playerId ? (
                                <PlayerAvatar
                                    player={{
                                        id: player.id,
                                        username: player.username,
                                    }}
                                    hasSubmitted={submittedPlayers.includes(
                                        player.id
                                    )}
                                />
                            ) : null}
                        </div>
                    ))
                ) : (
                    <p>No players available</p>
                )}
            </div>

            {/* Section de la SkullCard du joueur courant */}
            {playerId !== null &&
                players.some((player) => player.id === playerId) && (
                    <div className="skull-card mt-6">
                        <SkullCardInput
                            word={word}
                            setWord={setWord}
                            handleValidate={handleValidate}
                        />
                    </div>
                )}
        </div>
    );
};

export default GameTable;
