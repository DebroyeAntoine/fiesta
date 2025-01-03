import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import SkullWordCard from "../components/SkullWordCard";
import ScoreDisplay from "../components/ScoreDisplay";
import WordEvolutionReveal from "../components/WordEvolution";
import { useSocket } from "../context/SocketContext";

const GameOverPage: React.FC = () => {
    const location = useLocation();
    const socket = useSocket();
    const {
        characters = [],
        skullWords = [],
        game_id = 0,
    }: {
        characters: string[];
        skullWords: string[];
        game_id: number;
    } = location.state || {};

    const [selectedCharacters, setSelectedCharacters] = useState<
        Array<string | null>
    >(Array(skullWords.length).fill(null));
    const [waiting, setWaiting] = useState(false);
    const [score, setScore] = useState<number | null>(null);
    const [isOwner, setIsOwner] = useState<boolean>(false);
    const [gameResultReceived, setGameResultReceived] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleCharacterSelect = (index: number, character: string) => {
        const newSelections = [...selectedCharacters];
        newSelections[index] = character;
        setSelectedCharacters(newSelections);
    };

    const handleFinalSubmit = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            console.error("No JWT token found.");
            return;
        }

        try {
            const response = await fetch(
                `/game_api/game/${game_id}/submit_associations`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        associations: skullWords.map((word, index) => ({
                            skull_word: word,
                            selected_character: selectedCharacters[index],
                        })),
                    }),
                }
            );

            if (response.ok) {
                const data = await response.json();
                setIsOwner(data.isOwner);

                // Only set waiting to true if game result hasn't been received
                if (!gameResultReceived) {
                    setWaiting(true);
                }
            } else {
                console.error("Error submitting associations");
            }
        } catch (error) {
            console.error("Network error:", error);
        }
    };

    useEffect(() => {
        if (socket) {
            const handleGameResult = (data: {
                score: number;
                result: boolean;
            }) => {
                setScore(data.score);
                setSuccess(data.result);
                setGameResultReceived(true);
                setWaiting(false); // Always set waiting to false when game result is received
            };

            socket.on("game_result", handleGameResult);

            return () => {
                socket.off("game_result", handleGameResult);
            };
        }
    }, [socket]);

    const allSelected = selectedCharacters.every(
        (selection) => selection !== null
    );

    return (
        <div className="game-over-page relative flex flex-col items-center justify-center min-h-screen bg-navy text-white">
            <h1 className="text-4xl font-bold mb-8">
                Fin du Jeu : Associez les personnages
            </h1>

            {/* Overlay en attente */}
            {waiting && score === null && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50">
                    <div className="text-center text-2xl text-white p-6 bg-gray-800 bg-opacity-90 shadow-lg rounded-lg">
                        <p>En attente de validation des autres joueurs...</p>
                    </div>
                </div>
            )}

            {score != null ? (
                <>
                    <WordEvolutionReveal game_id={game_id} />
                    <ScoreDisplay
                        score={score}
                        isOwner={isOwner}
                        result={success}
                        game_id={game_id}
                    />
                </>
            ) : (
                <>
                    <div className="skull-word-cards grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                        {skullWords.map((word: string, index: number) => (
                            <SkullWordCard
                                key={index}
                                word={word}
                                characters={characters}
                                onSelect={(character: string) =>
                                    handleCharacterSelect(index, character)
                                }
                                selectedCharacter={selectedCharacters[index]}
                            />
                        ))}
                    </div>
                    <button
                        onClick={handleFinalSubmit}
                        className={`mt-8 bg-green-500 text-white px-6 py-2 rounded ${!allSelected ? "opacity-50 cursor-not-allowed" : ""}`}
                        disabled={!allSelected}
                    >
                        Valider toutes les associations
                    </button>
                </>
            )}
        </div>
    );
};

export default GameOverPage;
