import React, { useState, useEffect } from "react";

interface WordEvolutionProps {
    game_id: number;
}

interface WordEvolutionItem {
    player_id: number;
    username: string;
    word: string;
    round_number: number;
    character?: string;
}

interface ChainData {
    initialCharacter: string;
    steps: {
        username: string;
        word: string;
        roundNumber: number;
    }[];
}

const WordEvolutionChain: React.FC<WordEvolutionProps> = ({ game_id }) => {
    const [chains, setChains] = useState<ChainData[]>([]);
    const [currentChain, setCurrentChain] = useState<number>(0);
    const [isRevealing, setIsRevealing] = useState<boolean>(false);
    const [currentStep, setCurrentStep] = useState<number>(0);

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

                // Organiser les données par chaîne d'évolution
                const chainsMap = new Map<string, ChainData>();

                data.word_evolution.forEach((item: WordEvolutionItem) => {
                    if (item.round_number === 1) {
                        // C'est un mot initial, donc le début d'une nouvelle chaîne
                        chainsMap.set(item.word, {
                            initialCharacter:
                                item.character || "Personnage inconnu",
                            steps: [
                                {
                                    username: item.username,
                                    word: item.word,
                                    roundNumber: item.round_number,
                                },
                            ],
                        });
                    } else {
                        // Convertir les valeurs de la Map en tableau pour l'itération
                        Array.from(chainsMap.values()).forEach((chain) => {
                            if (chain.steps.length === item.round_number - 1) {
                                chain.steps.push({
                                    username: item.username,
                                    word: item.word,
                                    roundNumber: item.round_number,
                                });
                            }
                        });
                    }
                });

                setChains(Array.from(chainsMap.values()));
            }
        };
        fetchEvolutionData();
    }, [game_id]);

    const startReveal = () => {
        setIsRevealing(true);
        setCurrentStep(0);
        setCurrentChain(0);
    };

    const nextStep = () => {
        if (currentStep < 3) {
            setCurrentStep((prev) => prev + 1);
        } else if (currentChain < chains.length - 1) {
            setCurrentChain((prev) => prev + 1);
            setCurrentStep(0);
        }
    };

    if (chains.length === 0) return null;

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
                        <h2 className="text-2xl font-bold text-black">
                            Personnage {currentChain + 1}/{chains.length} -
                            Personnage: {chains[currentChain].initialCharacter}
                        </h2>
                        <button
                            onClick={nextStep}
                            disabled={
                                currentChain >= chains.length - 1 &&
                                currentStep >= 3
                            }
                            className="bg-green-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                        >
                            {currentStep < 3
                                ? "Mot suivant"
                                : "Personnage suivant"}
                        </button>
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg">
                        <div className="flex space-x-4 items-center">
                            {chains[currentChain].steps
                                .slice(0, currentStep + 1)
                                .map((step, index) => (
                                    <div
                                        key={index}
                                        className="flex items-center"
                                    >
                                        <div className="bg-gray-700 p-4 rounded">
                                            <p className="text-sm text-gray-400">
                                                Écrit par {step.username}
                                            </p>
                                            <p className="font-bold text-white text-lg">
                                                {step.word}
                                            </p>
                                        </div>
                                        {index < currentStep && (
                                            <div className="mx-2 text-white">
                                                →
                                            </div>
                                        )}
                                    </div>
                                ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WordEvolutionChain;
