import React from 'react';
import SkullCardDisplay from './SkullCardDisplay';
import CharacterCard from './CharacterCard';

interface SkullWordCardProps {
  word: string;
  characters: string[];
  onSelect: (selectedCharacter: string) => void;
  selectedCharacter: string | null;
}

const SkullWordCard: React.FC<SkullWordCardProps> = ({ word, characters, onSelect, selectedCharacter }) => {
  return (
    <div className="skull-word-card flex flex-col items-center">
      <SkullCardDisplay word={word} />
      <div className="characters mt-4 grid grid-cols-2 gap-4">
        {characters.map((character) => (
          <CharacterCard
            key={character}
            name={character}
            onSelect={() => onSelect(character)}
            isSelected={selectedCharacter === character}
          />
        ))}
      </div>
    </div>
  );
};

export default SkullWordCard;

