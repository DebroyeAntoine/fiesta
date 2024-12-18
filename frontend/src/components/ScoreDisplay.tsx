import React, { useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";

interface ScoreDisplayProps {
    score: number;
    isOwner: boolean;
    result: boolean;
    game_id: number;
}
interface Game {
    game_id: string;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({
    score,
    isOwner,
    result,
    game_id,
}) => {
    const socket = useSocket();
    const navigate = useNavigate();

    const leaveGame = useCallback(() => {
        const token = localStorage.getItem("token");
        socket.emit("leave_game", {
            game_id: game_id,
            player_token: token,
        });
    }, [socket, game_id]);
    const handleQuit = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No JWT token found");
            return;
        }

        try {
            const response = await fetch(`/game/${game_id}/quit`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ result: result }),
            });
            if (response.ok) {
                navigate(`/gameList`);
            }
        } catch (error) {}
    };
    const handleCreateNewGame = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No JWT token found");
            return;
        }

        try {
            const response = await fetch(`/game/${game_id}/remake`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ result: result }),
            });
            if (response.ok) {
                const data = await response.json();
                navigate(`/game/${data.game_id}/lobby`);
            }
        } catch (error) {}
    };
    useEffect(() => {
        const socketListeners = {
            new_game: (data: Game) => {
                console.log(data);
                socket.emit("join_game", {
                    token: localStorage.getItem("token"),
                    game_id: data.game_id,
                });
                navigate(`/game/${data.game_id}/lobby`);
            },
            go_to_menu: () => {
                navigate("/gameList");
            },
        };
        Object.entries(socketListeners).forEach(([event, handler]) => {
            socket.on(event, handler);
        });

        return () => {
            Object.entries(socketListeners).forEach(([event, handler]) => {
                socket.off(event, handler);
            });

            leaveGame();
        };
    }, [socket, leaveGame, navigate]);
    return (
        <div className="score-section text-center text-black">
            <h2 className="text-3xl mb-6">Votre Score Final :</h2>
            <p className="text-2xl">{score} points</p>
            {isOwner && (
                <div className="flex gap-4">
                    <button
                        onClick={() => {
                            handleQuit();
                        }}
                        className="mt-4 w-full bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition duration-200"
                    >
                        Go to the menu
                    </button>
                    <button
                        onClick={() => {
                            handleCreateNewGame();
                        }}
                        className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-200"
                    >
                        Create New Game
                    </button>
                </div>
            )}
        </div>
    );
};

export default ScoreDisplay;
