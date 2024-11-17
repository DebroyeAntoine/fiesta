// src/pages/Lobby.tsx
import React, { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import PlayerList from "../components/PlayerList";
import StartGameButton from "../components/StartGameButton";

const Lobby: React.FC = () => {
    const { gameId } = useParams<{ gameId: string }>();
    const socket = useSocket();
    const [players, setPlayers] = useState([]);
    const [isOwner, setIsOwner] = useState(false);
    const [isReady, setIsReady] = useState(false);
    const navigate = useNavigate();

    // Référence pour savoir si la redirection a eu lieu
    const isRedirected = useRef(false);

    // Effet pour gérer les actions liées au jeu et à la redirection
    useEffect(() => {
        const handleGameStarted = () => {
            console.log("Game started");
            isRedirected.current = true; // Indique qu'une redirection est en cours
        };

        const fetchGames = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await fetch(`/game/${gameId}/get_lobby`, {
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
        };

        // Charger les informations sur la partie
        fetchGames();

        // Abonnement aux événements du socket
        socket.on("player_joined", (data) => {
            console.log(data.player);
        });
        socket.on("players_update", (data) => setPlayers(data));
        socket.on("changing_ownership", () => {
            console.log("Ownership changed");
            fetchGames(); // Recharger les données
        });
        socket.on("player_left", (data) => setPlayers(data.players));
        socket.on("player_ready_update", (data) => setPlayers(data.players));
        socket.on("game_started", handleGameStarted);
        socket.on("game_info", (data) =>
            setIsOwner(data.owner_id === socket.id)
        );

        // Nettoyage des événements à la destruction
        return () => {
            console.log(`Cleanup, redirect: ${isRedirected.current}`);
            if (!isRedirected.current) {
                // Émettre leave_game seulement si on n'a pas été redirigé
                //        socket.emit('leave_game', { game_id: gameId, player_token: localStorage.getItem('token') });
            }

            // Nettoyage des événements du socket
            socket.off("player_joined");
            socket.off("player_left");
            socket.off("players_update");
            socket.off("game_started");
            socket.off("game_info");
        };
    }, [gameId, socket]); // Dépendances : le gameId et socket

    // Fonction pour démarrer le jeu et rediriger après
    const handleStartGame = async () => {
        const token = localStorage.getItem("token");
        const response = await fetch(`/game/${gameId}/start`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            console.log("Game started, redirecting...");
            isRedirected.current = true; // Indiquer que le jeu est démarré, donc redirection
            navigate(`/game/${gameId}`); // Rediriger vers la page du jeu après démarrage
        } else {
            console.error("Error when starting the game");
        }
    };

    // Effet pour gérer la redirection après que le jeu commence (si nécessaire)
    useEffect(() => {
        if (isRedirected.current) {
            console.log("Redirecting to game...");
            // La redirection se fait dans `handleStartGame` maintenant.
        }
    }, [gameId]);

    // Fonction pour gérer l'état prêt
    const handleReady = () => {
        socket.emit("player_ready", { game_id: gameId });
        setIsReady(!isReady);
    };

    return (
        <div className="lobby-page bg-yellow-100 min-h-screen p-6 flex flex-col items-center">
            <h1 className="text-3xl text-orange-600 font-bold mb-4">
                🎉 Lobby - Game {gameId} 🎉
            </h1>
            {/* Affichage des joueurs dans la salle */}
            <PlayerList players={players} />
            {/* Bouton de démarrage de jeu visible seulement pour l'hôte */}
            {isOwner && <StartGameButton onClick={handleStartGame} />}
            {/* Bouton prêt pour le joueur */}
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
