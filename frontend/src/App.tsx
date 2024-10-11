// src/App.tsx
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import GameBoard from './components/GameBoard';
import './styles.css';

const App: React.FC = () => {
    const [message, setMessage] = useState<string>('');

    useEffect(() => {
        fetch('http://127.0.0.1:5000/')
            .then(res => res.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div className="App">
            <Header message={message} />
            <GameBoard />
        </div>
    );
}

export default App;

