import React from 'react';
import AuthForm from './AuthForm';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
    const navigate = useNavigate();
    const handleLogin = async (username: string, password: string) => {
        const response = await fetch('/auth_api/login', {
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
            navigate('/gameList');
            //navigate(`/game/${data.gameId}`);
        }
    };

    return <AuthForm onSubmit={handleLogin} isRegister={false} />;
};

export default Login;

