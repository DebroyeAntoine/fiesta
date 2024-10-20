import React, { useEffect, useState } from 'react';

interface InitialWordDisplayProps {
  gameId: string; // ou string, selon le type que tu attends pour gameId
}

const InitialWordDisplay: React.FC<InitialWordDisplayProps> = ({ gameId }) => {
  const [initialWord, setInitialWord] = useState('');

  useEffect(() => {
    const fetchInitialWord = async () => {
      const response = await fetch(`/game/${gameId}/current_round`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Si tu utilises JWT
        },
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setInitialWord(data.initial_word);
      } else {
        console.error('Failed to fetch initial word');
      }
    };

    fetchInitialWord();
  }, [gameId]);

  return (
    <div className="initial-word-display bg-blue-100 p-4 rounded-lg shadow-md mb-4">
      <h2 className="text-lg font-semibold">Mot Initial</h2>
      <span className="font-bold">{initialWord}</span>
    </div>
  );
};

export default InitialWordDisplay;

