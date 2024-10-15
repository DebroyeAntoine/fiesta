import React, { useState } from 'react';
import PlayerAvatar from './PlayerAvatar';
import SkullCard from './SkullCard';

const GameTable = () => {
  const [word, setWord] = useState('');  // Le mot ou l'indice affiché sur la carte tête de mort
  const [players, setPlayers] = useState([
    { id: 1, name: 'Player 1', hasValidated: false },
    { id: 2, name: 'Player 2', hasValidated: false },
    { id: 3, name: 'Player 3', hasValidated: false },
    { id: 4, name: 'Player 4', hasValidated: false },
  ]);

  const handleValidate = () => {
    // Valider le mot ou l'indice et l'envoyer au back-end
    console.log('Word/indice submitted:', word);
      // TODO handle backend.
  };

  return (
    <div className="game-table relative w-full h-screen flex justify-center items-center">
      <div className="center-skull-card absolute bottom-10">
        <SkullCard word={word} setWord={setWord} handleValidate={handleValidate} />
      </div>

      <div className="player-circle grid grid-cols-4 gap-4">
        {players.map((player) => (
          <PlayerAvatar key={player.id} player={player} />
        ))}
      </div>
    </div>
  );
};

export default GameTable;

