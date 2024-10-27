import React from 'react';
import { useLocation } from 'react-router-dom';
import SkullWordCard from '../components/SkullWordCard';


const GameOverPage: React.FC = () => {

  const location = useLocation();
  const { characters = [], skullWords = [] } = location.state || {};
  console.log("Characters:", characters);
  const handleSubmit = (skullIndex: number, selectedCharacter: string) => {
    console.log(`Le mot "${skullWords[skullIndex]}" a été associé à "${selectedCharacter}"`);
  };

  return (
    <div className="game-over-page flex flex-col items-center justify-center min-h-screen bg-navy text-white">
      <h1 className="text-4xl font-bold mb-8">Fin du Jeu : Associez les personnages</h1>
      <div className="skull-word-cards grid grid-cols-1 md:grid-cols-3 gap-8">
        {skullWords.map((word: string, index: number) => (
          <SkullWordCard
            key={index}
            word={word}
            characters={characters}
            onSubmit={(selectedCharacter) => handleSubmit(index, selectedCharacter)}
          />
        ))}
      </div>
    </div>
  );
};

export default GameOverPage;

