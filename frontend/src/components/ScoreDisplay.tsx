import React from "react";
import { useNavigate } from "react-router-dom";

interface ScoreDisplayProps {
    score: number;
    isOwner: boolean;
    result: boolean;
    game_id: number;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({
    score,
    isOwner,
    result,
    game_id,
}) => {
    const navigate = useNavigate();
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
                navigate(`/game/${data.game_id}`);
            }
        } catch (error) {}
    };
    return (
        <div className="score-section text-center text-black">
            <h2 className="text-3xl mb-6">Votre Score Final :</h2>
            <p className="text-2xl">{score} points</p>
            {isOwner && (
                <div className="flex gap-4">
                    <button
                        onClick={() => {
                            console.log("coucou");
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
