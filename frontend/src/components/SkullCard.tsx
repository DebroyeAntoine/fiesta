import React from 'react';

interface SkullCardProps {
  word: string;
  setWord: (value: string) => void;
  handleValidate: () => void;
}

const SkullCard: React.FC<SkullCardProps> = ({ word, setWord, handleValidate }) => {
  return (
    <div className="bg-primary p-6 rounded-lg shadow-md text-center">
      <h3 className="text-xl font-bold text-white">Carte Tête de Mort</h3>
      <input
        type="text"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        placeholder="Entrez votre indice"
        className="mt-4 p-2 border border-secondary rounded w-full"
      />
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

