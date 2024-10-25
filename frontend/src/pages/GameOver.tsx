import React from 'react';
import SkullWordCard from '../components/SkullWordCard';

// Mock data (à remplacer par des données réelles)
const skullWords = ['Fantôme', 'Pirate', 'Vampire', 'Maths']; // Derniers mots soumis
const characters = ['Casper', 'Jack Sparrow', 'Dracula', 'Pythagore', 'Piège 1', 'Piège 2']; // Personnages + pièges

const GameOverPage: React.FC = () => {
  const handleSubmit = (skullIndex: number, selectedCharacter: string) => {
    console.log(`Le mot "${skullWords[skullIndex]}" a été associé à "${selectedCharacter}"`);
    // Ici, tu peux envoyer les choix au backend via WebSocket ou API
  };

  return (
    <div className="game-over-page flex flex-col items-center justify-center min-h-screen bg-navy text-white">
      <h1 className="text-4xl font-bold mb-8">Fin du Jeu : Associez les personnages</h1>
      <div className="skull-word-cards grid grid-cols-1 md:grid-cols-3 gap-8">
        {skullWords.map((word, index) => (
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

