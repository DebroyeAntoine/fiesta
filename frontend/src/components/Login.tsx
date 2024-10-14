import React from 'react';
import AuthForm from './AuthForm';

const Login: React.FC = () => {
    const handleLogin = async (username: string, password: string) => {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Failed to login');
        }
    };

    return <AuthForm onSubmit={handleLogin} isRegister={false} />;
};

export default Login;

