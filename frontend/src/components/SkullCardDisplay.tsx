import React from 'react';
import SkullCardBase from './SkullCardBase';

interface SkullCardDisplayProps {
  word: string;
}

const SkullCardDisplay: React.FC<SkullCardDisplayProps> = ({ word }) => (
  <SkullCardBase>
    <div className="w-full p-2 mt-4 bg-gray-200 rounded-lg flex justify-center items-center">
      <p className="text-xl font-bold text-center text-black">{word}</p>
    </div>
  </SkullCardBase>
);

export default SkullCardDisplay;

