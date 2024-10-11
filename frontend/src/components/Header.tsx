// src/components/Header.tsx
import React from 'react';

interface HeaderProps {
    message: string;
}

const Header: React.FC<HeaderProps> = ({ message }) => {
    return (
        <header>
            <h1>Fiesta de los Muertos</h1>
            <p>{message}</p>
        </header>
    );
}

export default Header;

