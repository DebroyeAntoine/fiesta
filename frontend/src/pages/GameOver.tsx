import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import SkullWordCard from '../components/SkullWordCard';

const GameOverPage: React.FC = () => {
  const location = useLocation();
  const { characters = [], skullWords = [] }: { characters: string[]; skullWords: string[] } = location.state || {};

  const [selectedCharacters, setSelectedCharacters] = useState<Array<string | null>>(Array(skullWords.length).fill(null));

  const handleCharacterSelect = (index: number, character: string) => {
    const newSelections = [...selectedCharacters];
    newSelections[index] = character;
    setSelectedCharacters(newSelections);
  };

  const handleFinalSubmit = () => {
    console.log("Associations finales:", selectedCharacters);
    // TODO: Envoyer les données au backend ici pour sauvegarder les choix
  };

  const allSelected = selectedCharacters.every((selection) => selection !== null);

  return (
    <div className="game-over-page flex flex-col items-center justify-center min-h-screen bg-navy text-white">
      <h1 className="text-4xl font-bold mb-8">Fin du Jeu : Associez les personnages</h1>
      <div className="skull-word-cards grid grid-cols-1 md:grid-cols-3 gap-8">
        {skullWords.map((word: string, index: number) => (
          <SkullWordCard
            key={index}
            word={word}
            characters={characters}
            onSelect={(character: string) => handleCharacterSelect(index, character)}
            selectedCharacter={selectedCharacters[index]}
          />
        ))}
      </div>
      <button
        onClick={handleFinalSubmit}
        className={`mt-8 bg-green-500 text-white px-6 py-2 rounded ${!allSelected ? 'opacity-50 cursor-not-allowed' : ''}`}
        disabled={!allSelected}
      >
        Valider toutes les associations
      </button>
    </div>
  );
};

export default GameOverPage;

