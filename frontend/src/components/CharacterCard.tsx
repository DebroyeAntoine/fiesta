import React from 'react';

interface CharacterCardProps {
  name: string;
  onSelect: () => void;
  isSelected: boolean;
}

const CharacterCard: React.FC<CharacterCardProps> = ({ name, onSelect, isSelected }) => {
  return (
    <div
      className={`p-4 bg-white rounded-xl shadow-md cursor-pointer transition-all duration-300 border-2 ${isSelected ? 'border-green-500' : 'border-gray-800'}`}
      onClick={onSelect}
    >
      <p className="text-center font-bold text-xl text-black">{name}</p>
    </div>
  );
};

export default CharacterCard;

