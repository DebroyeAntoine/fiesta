import React from 'react';

interface ScoreDisplayProps {
  score: number;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score }) => {
  return (
    <div className="score-section text-center text-black">
      <h2 className="text-3xl mb-6">Votre Score Final :</h2>
      <p className="text-2xl">{score} points</p>
    </div>
  );
};

export default ScoreDisplay;
