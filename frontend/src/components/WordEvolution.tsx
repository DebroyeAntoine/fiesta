import React, { useState, useEffect } from "react";
import { useSocket } from "../context/SocketContext";

interface WordEvolutionProps {
    game_id: number;
//    isOwner: boolean;
}

interface WordEvolutionItem {
    player_id: number;
    username: string;
    word: string;
    round_number: number;
}

interface PlayerWordData {
    username: string;
    words: (string | null)[];
}

interface OrganizedData {
    [key: number]: {
        username: string;
        words: (string | null)[];
    };
}

const WordEvolutionReveal: React.FC<WordEvolutionProps> = ({ game_id }) => {
    const [evolutionData, setEvolutionData] = useState<PlayerWordData[]>([]);
    const [currentStep, setCurrentStep] = useState<number>(0);
    const [isRevealing, setIsRevealing] = useState<boolean>(false);

    useEffect(() => {
        const fetchEvolutionData = async () => {
            const token = localStorage.getItem("token");
            const response = await fetch(
                `/game_api/game/${game_id}/word_evolution`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (response.ok) {
                const data = await response.json();
                const organizedData: OrganizedData = data.word_evolution.reduce(
                    (acc: OrganizedData, item: WordEvolutionItem) => {
                        if (!acc[item.player_id]) {
                            acc[item.player_id] = {
                                username: item.username,
                                words: Array(4).fill(null),
                            };
                        }
                        acc[item.player_id].words[item.round_number - 1] =
                            item.word;
                        return acc;
                    },
                    {}
                );
                setEvolutionData(Object.values(organizedData));
            }
        };
        fetchEvolutionData();
    }, [game_id]);

    const startReveal = () => {
        setIsRevealing(true);
        setCurrentStep(0);
    };

    const nextStep = () => {
        if (currentStep < 4) {
            setCurrentStep((prev) => prev + 1);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-4">
            {!isRevealing ? (
                <button
                    onClick={startReveal}
                    className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
                >
                    Révéler l'évolution des mots
                </button>
            ) : (
                <div className="space-y-6">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-bold text-white">
                            Tour {currentStep + 1}/4
                        </h2>
                        <button
                            onClick={nextStep}
                            disabled={currentStep >= 4}
                            className="bg-green-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                        >
                            Tour suivant
                        </button>
                    </div>

                    <div className="grid gap-4">
                        {evolutionData.map((player, index) => (
                            <div
                                key={index}
                                className="bg-gray-800 p-4 rounded-lg"
                            >
                                <h3 className="text-xl font-semibold mb-2 text-white">
                                    {player.username}
                                </h3>
                                <div className="flex space-x-4">
                                    {player.words
                                        .slice(0, currentStep + 1)
                                        .map((word, wordIndex) => (
                                            <div
                                                key={wordIndex}
                                                className="bg-gray-700 p-3 rounded text-center min-w-[100px]"
                                            >
                                                <span className="text-sm text-gray-400">
                                                    Tour {wordIndex + 1}
                                                </span>
                                                <p className="font-bold text-white">
                                                    {word}
                                                </p>
                                            </div>
                                        ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default WordEvolutionReveal;
