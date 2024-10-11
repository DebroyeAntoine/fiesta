// src/components/GameBoard.tsx
import React, { useState } from 'react';
import PlayerInput from './PlayerInput';
import Result from './Result';

const GameBoard: React.FC = () => {
    const [result, setResult] = useState<{ message: string } | null>(null);

    const handleResult = (data: { message: string }) => {
        setResult(data);
    };

    return (
        <div>
            <h2>Tableau de jeu</h2>
            <PlayerInput onResult={handleResult} />
            {result && <Result result={result} />}
        </div>
    );
}

export default GameBoard;

