import React, { useEffect, useState, useCallback, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import PlayerList from "../components/PlayerList";
import StartGameButton from "../components/StartGameButton";

interface PlayerJoinedData {
    player: {
        id: string;
        username: string;
    };
}

interface PlayersUpdateData {
    players: Array<{
        id: string;
        username: string;
    }>;
}

interface GameInfoData {
    owner_id: string;
}

const Lobby: React.FC = () => {
    const { gameId } = useParams<{ gameId: string }>();
    const socket = useSocket();
    const [players, setPlayers] = useState<PlayersUpdateData["players"]>([]);
    const [isOwner, setIsOwner] = useState(false);
    const [isReady, setIsReady] = useState(false);
    const navigate = useNavigate();

    const isRedirecting = useRef(false);

    const leaveGame = useCallback(() => {
        if (!isRedirecting.current) {
            const token = localStorage.getItem("token");
            socket.emit("leave_game", {
                game_id: gameId,
                player_token: token,
            });
        }
    }, [socket, gameId]);

    const fetchLobbyInfo = useCallback(async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`/game_api/game/${gameId}/get_lobby`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setPlayers(data.players);
                setIsOwner(data.isOwner);
            }
        } catch (error) {
            console.error("Error fetching games", error);
        }
    }, [gameId]);

    const handleStartGame = useCallback(async () => {
        const token = localStorage.getItem("token");
        try {
            const response = await fetch(`/game_api/game/${gameId}/start`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                isRedirecting.current = true;
                navigate(`/game/${gameId}`);
            } else {
                console.error("Error when starting the game");
            }
        } catch (error) {
            console.error("Error starting game", error);
        }
    }, [gameId, navigate]);

    const handleReady = useCallback(() => {
        socket.emit("player_ready", { game_id: gameId });
        setIsReady((prev) => !prev);
    }, [socket, gameId]);

    useEffect(() => {
        fetchLobbyInfo();

        const socketListeners = {
            player_joined: (data: PlayerJoinedData) => console.log(data.player),
            players_update: (data: PlayersUpdateData) =>
                setPlayers(data.players),
            changing_ownership: () => {
                console.log("Ownership changed");
                fetchLobbyInfo();
            },
            player_left: (data: PlayersUpdateData) => setPlayers(data.players),
            player_ready_update: (data: PlayersUpdateData) =>
                setPlayers(data.players),
            game_started: () => {
                isRedirecting.current = true;
                navigate(`/game/${gameId}`);
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
    }, [socket, gameId, fetchLobbyInfo, leaveGame, navigate]);

    return (
        <div className="lobby-page bg-yellow-100 min-h-screen p-6 flex flex-col items-center">
            <h1 className="text-3xl text-orange-600 font-bold mb-4">
                🎉 Lobby - Game {gameId} 🎉
            </h1>
            <PlayerList players={players} />
            {isOwner && <StartGameButton onClick={handleStartGame} />}
            <button
                onClick={handleReady}
                className="mt-4 bg-blue-500 text-white p-2 rounded"
            >
                {isReady ? "Ready" : "Not Ready"}
            </button>
        </div>
    );
};

export default Lobby;
