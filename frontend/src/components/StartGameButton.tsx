// src/components/StartGameButton.tsx
import React from 'react';

interface StartGameButtonProps {
  onClick: () => void;
}

const StartGameButton: React.FC<StartGameButtonProps> = ({ onClick }) => {
  return (
    <button
      className="start-game-button bg-purple-600 text-white py-2 px-8 rounded-full mt-4 hover:bg-purple-700 transition duration-300"
      onClick={onClick}
    >
      Start Game
    </button>
  );
};

export default StartGameButton;

