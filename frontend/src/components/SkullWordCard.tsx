import React, { useState } from 'react';
import SkullCardDisplay from './SkullCardDisplay';
import CharacterCard from './CharacterCard';

interface SkullWordCardProps {
  word: string;
  characters: string[];
  onSubmit: (selectedCharacter: string) => void;
}

const SkullWordCard: React.FC<SkullWordCardProps> = ({ word, characters, onSubmit }) => {
  const [selectedCharacter, setSelectedCharacter] = useState<string | null>(null);

  const handleSelectCharacter = (character: string) => {
    setSelectedCharacter(character);
  };

  const handleSubmit = () => {
    if (selectedCharacter) {
      onSubmit(selectedCharacter);
    }
  };

  return (
    <div className="skull-word-card flex flex-col items-center">
      {/* Carte Tête de mort */}
      <SkullCardDisplay word={word} />
      {/* Sélection des personnages */}
      <div className="characters mt-4 grid grid-cols-2 gap-4">
        {characters.map((character) => (
          <CharacterCard
            key={character}
            name={character}
            onSelect={() => handleSelectCharacter(character)}
            isSelected={selectedCharacter === character}
          />
        ))}
      </div>
      {/* Bouton de soumission */}
      <button
        onClick={handleSubmit}
        className={`mt-4 bg-green-500 text-white px-6 py-2 rounded ${!selectedCharacter && 'opacity-50 cursor-not-allowed'}`}
        disabled={!selectedCharacter}
      >
        Valider
      </button>
    </div>
  );
};

export default SkullWordCard;

