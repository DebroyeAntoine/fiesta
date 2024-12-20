import React, { useEffect, useState } from "react";

interface InitialWordDisplayProps {
    gameId: string;
    refreshKey: boolean;
}

const InitialWordDisplay: React.FC<InitialWordDisplayProps> = ({
    gameId,
    refreshKey,
}) => {
    const [initialWord, setInitialWord] = useState("");

    useEffect(() => {
        const fetchInitialWord = async () => {
            try {
                const response = await fetch(
                    `/game_api/game/${gameId}/current_round`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    setInitialWord(data.initial_word);
                } else {
                    console.error("Failed to fetch initial word");
                }
            } catch (error) {
                console.error("Error fetching initial word:", error);
            }
        };

        fetchInitialWord();
    }, [gameId, refreshKey]);

    return (
        <div className="relative mx-auto p-6 mt-6 rounded-lg shadow-lg max-w-md bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 border-4 border-yellow-300 text-white text-center font-bold text-3xl">
            <h2 className="text-4xl mb-2 drop-shadow-lg">Mot Initial</h2>
            <span className="block text-2xl font-extrabold drop-shadow-md animate-bounce">
                {initialWord || "Chargement..."}
            </span>

            {/* Confetti Animation */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden">
                {Array.from({ length: 50 }).map((_, index) => (
                    <div
                        key={index}
                        className="confetti absolute w-2 h-2 opacity-75 animate-confetti-fall"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `-${Math.random() * 100}px`,
                            backgroundColor:
                                index % 2 === 0
                                    ? "rgba(255, 165, 0, 0.9)"
                                    : "rgba(255, 69, 0, 0.9)",
                            animationDelay: `${Math.random() * 3}s`,
                            animationDuration: `${2 + Math.random() * 3}s`,
                        }}
                    />
                ))}
            </div>
        </div>
    );
};

export default InitialWordDisplay;
