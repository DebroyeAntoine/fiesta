import React from "react";

interface ScoreDisplayProps {
    score: number;
    isOwner: boolean;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score, isOwner }) => {
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
                        Quit the game
                    </button>
                    <button
                        onClick={() => {
                            console.log("coucou");
                        }}
                        className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition duration-200"
                    >
                        Create New Game
                    </button>
                </div>
            )}
        </div>
    );
};

export default ScoreDisplay;
