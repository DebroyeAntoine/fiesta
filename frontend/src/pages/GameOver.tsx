import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import SkullWordCard from '../components/SkullWordCard';
import { useSocket } from '../context/SocketContext';

const GameOverPage: React.FC = () => {
  const location = useLocation();
  const socket = useSocket();
  const { characters = [], skullWords = [] }: { characters: string[]; skullWords: string[] } = location.state || {};
  const [selectedCharacters, setSelectedCharacters] = useState<Array<string | null>>(Array(skullWords.length).fill(null));
  const [waiting, setWaiting] = useState(false);
  const [scores, setScores] = useState<{ [playerId: number]: number } | null>(null);

  const handleCharacterSelect = (index: number, character: string) => {
    const newSelections = [...selectedCharacters];
    newSelections[index] = character;
    setSelectedCharacters(newSelections);
  };

  const handleFinalSubmit = () => {
    if (socket) {
      socket.emit('submit_associations', {
        game_id: location.state.gameId,
        player_id: location.state.playerId,
        associations: skullWords.map((word, index) => ({
          skull_word: word,
          selected_character: selectedCharacters[index],
        })),
      });
      setWaiting(true); // Afficher l'écran d'attente après envoi
    }
  };

  useEffect(() => {
    if (socket) {
      socket.on('game_over_scores', (data) => {
        setScores(data.scores);
        setWaiting(false);
      });

      return () => {
        socket.off('game_over_scores');
      };
    }
  }, [socket]);

  const allSelected = selectedCharacters.every((selection) => selection !== null);

  return (
    <div className="game-over-page relative flex flex-col items-center justify-center min-h-screen bg-navy text-white">
      <h1 className="text-4xl font-bold mb-8">Fin du Jeu : Associez les personnages</h1>

      {/* Overlay en attente */}
      {waiting && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50">
          <div className="text-center text-2xl text-white p-6 bg-gray-800 bg-opacity-90 shadow-lg rounded-lg">
            <p>En attente de validation des autres joueurs...</p>
          </div>
        </div>
      )}

      {scores ? (
        <div className="scores-section text-center">
          <h2 className="text-3xl mb-6">Scores finaux</h2>
          <ul>
            {Object.entries(scores).map(([playerId, score]) => (
              <li key={playerId}>Joueur {playerId} : {score} points</li>
            ))}
          </ul>
        </div>
      ) : (
        <>
          <div className="skull-word-cards grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
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
        </>
      )}
    </div>
  );
};

export default GameOverPage;

