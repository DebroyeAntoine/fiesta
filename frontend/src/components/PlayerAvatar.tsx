import React from 'react';

interface PlayerAvatarProps {
  player: {
    id: number;
    name: string;
  };
  hasSubmitted: boolean;
}

const PlayerAvatar: React.FC<PlayerAvatarProps> = ({ player, hasSubmitted }) => {
  return (
    <div className={`player-avatar ${hasSubmitted ? 'bg-green-400' : 'bg-gray-400'} p-4 rounded-full flex flex-col items-center`}>
      <p className="text-white font-bold">{player.name}</p>
      {!hasSubmitted ? (
        <span className="animate-bounce text-2xl">...</span>
      ) : (
        <span className="text-2xl">✔️</span>
      )}
    </div>
  );
};

export default PlayerAvatar;

