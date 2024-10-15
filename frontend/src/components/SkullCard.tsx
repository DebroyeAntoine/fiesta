import React from 'react';

interface SkullCardProps {
  word: string;
  setWord: (value: string) => void;
  handleValidate: () => void;
}

const SkullCard: React.FC<SkullCardProps> = ({ word, setWord, handleValidate }) => {return (
    <div className="relative w-48 h-60 bg-white rounded-xl shadow-md p-4 flex flex-col items-center justify-between border-2 border-gray-800">
      {/* Crâne */}
      <div className="w-full flex flex-col items-center relative">
        {/* Décorations supérieures */}
        <div className="absolute top-0 w-full flex justify-center">
          <div className="w-10 h-2 bg-yellow-500 rounded-full mr-2"></div>
          <div className="w-10 h-2 bg-red-500 rounded-full"></div>
        </div>
        {/* Yeux */}
        <div className="flex justify-between w-full mt-4">
          <div className="w-10 h-10 bg-black rounded-full border-4 border-orange-500"></div>
          <div className="w-10 h-10 bg-black rounded-full border-4 border-orange-500"></div>
        </div>
        {/* Nez */}
        <div className="w-4 h-6 bg-black rounded-b-full mt-2"></div>
        {/* Bouche */}
        <div className="mt-4 flex space-x-1">
          <div className="w-3 h-3 bg-black rounded-full"></div>
          <div className="w-3 h-3 bg-black rounded-full"></div>
          <div className="w-3 h-3 bg-black rounded-full"></div>
          <div className="w-3 h-3 bg-black rounded-full"></div>
        </div>
      </div>
      {/* Zone de texte */}
      <div className="w-full p-2 mt-4 bg-gray-200 rounded-lg flex justify-center items-center">
        <input
          type="text"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          className="bg-transparent border-none text-center text-xl font-bold outline-none" 
          placeholder="Type here" 
        />
      </div>
      <button
        onClick={handleValidate}
        className="mt-4 bg-secondary hover:bg-primary text-white font-semibold py-2 px-4 rounded transition duration-300 ease-in-out"
      >
        Valider
      </button>
    </div>
  );
};
export default SkullCard;

