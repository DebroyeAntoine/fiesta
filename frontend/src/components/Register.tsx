import React from 'react';
import AuthForm from './AuthForm';

const Register: React.FC = () => {
    const handleRegister = async (username: string, password: string) => {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Failed to register');
        }
    };

    const handleDeleteUsers = async () => {
        const response = await fetch('/delete', {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete users');
        }
    };

    return <AuthForm onSubmit={handleRegister} onDeleteUsers={handleDeleteUsers} isRegister={true} />;
};

export default Register;

