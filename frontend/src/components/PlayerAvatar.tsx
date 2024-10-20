import React from 'react';

interface PlayerAvatarProps {
  player: {
    id: number;
    username: string;
  };
  hasSubmitted: boolean;
}

const PlayerAvatar: React.FC<PlayerAvatarProps> = ({ player, hasSubmitted }) => {
  return (
    <div className={`player-avatar ${hasSubmitted ? 'bg-green-400' : 'bg-gray-400'}
      p-4 w-24 h-24 rounded-full flex flex-col items-center justify-center
      border-4 ${hasSubmitted ? 'border-green-600' : 'border-gray-500'}
      shadow-lg transition-all duration-300 ease-in-out transform ${!hasSubmitted && 'hover:scale-105'}`}>

      {/* Username */}
      <p className="text-white font-bold text-center truncate w-20">{player.username}</p>

      {/* Status Icon */}
      {!hasSubmitted ? (
        <span className="animate-pulse text-2xl mt-2">⏳</span>
      ) : (
        <span className="text-2xl mt-2">✔️</span>
      )}
    </div>
  );
};

export default PlayerAvatar;

