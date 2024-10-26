import React from 'react';
import AuthForm from './AuthForm';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
    const navigate = useNavigate();
    const handleLogin = async (username: string, password: string) => {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error('Failed to login');
        } else {
            localStorage.setItem('token', data.token);
            navigate(`/game/${data.gameId}/player/${data.playerId}/round/1`);
        }
    };

    return <AuthForm onSubmit={handleLogin} isRegister={false} />;
};

export default Login;

