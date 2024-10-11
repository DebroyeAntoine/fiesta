// src/components/Result.tsx
import React from 'react';

interface ResultProps {
    result: { message: string };
}

const Result: React.FC<ResultProps> = ({ result }) => {
    return (
        <div>
            <h3>Résultat</h3>
            <p>{result.message}</p>
        </div>
    );
}

export default Result;

