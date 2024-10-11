// src/components/PlayerInput.tsx
import React, { useState } from 'react';

interface PlayerInputProps {
    onResult: (data: { message: string }) => void;
}

const PlayerInput: React.FC<PlayerInputProps> = ({ onResult }) => {
    const [input, setInput] = useState<string>('');

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word: input }),
        })
            .then(res => res.json())
            .then(data => {
                onResult(data);
                setInput('');
            })
            .catch(error => console.error('Error submitting word:', error));
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                placeholder="Entrez votre mot ici" 
            />
            <button type="submit">Soumettre</button>
        </form>
    );
}

export default PlayerInput;

