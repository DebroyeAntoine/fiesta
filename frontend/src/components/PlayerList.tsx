// src/components/PlayerList.tsx
import React from 'react';


interface PlayerListProps {
    players: string[];
}

const PlayerList: React.FC<PlayerListProps> = ({ players }) => {
  return (
    <div className="player-list grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
      {players.map((player, index) => (
        <div
          key={index} // Utilise index comme clé puisque tu n'as plus les id
          className="player-item flex flex-col items-center p-4 bg-white rounded-lg shadow-lg transform transition duration-300 hover:scale-105 hover:bg-yellow-50"
        >
          <div className="player-avatar bg-white rounded-full border-4 border-pink-500 p-4 flex items-center justify-center text-orange-600 font-semibold shadow-lg">
            {player[0]}
          </div>
          <div className="mt-2 text-xl font-semibold text-orange-600">{player}</div>
        </div>
      ))}
    </div>
  );
};

export default PlayerList;

