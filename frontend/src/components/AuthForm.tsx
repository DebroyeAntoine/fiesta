import React, { useState } from 'react';

interface AuthFormProps {
    onSubmit: (username: string, password: string) => Promise<void>;
    onDeleteUsers?: () => Promise<void>;  // Prop facultative pour supprimer les utilisateurs
    isRegister: boolean;
}

const AuthForm: React.FC<AuthFormProps> = ({ onSubmit, onDeleteUsers, isRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await onSubmit(username, password);
            setMessage(isRegister ? "User registered successfully!" : "Login successful!");
        } catch (error) {
            setMessage("Error occurred");
        }
    };

    const handleDeleteUsers = async () => {
        if (onDeleteUsers) {
            try {
                await onDeleteUsers();
                setMessage("All users deleted successfully!");
            } catch (error) {
                setMessage("Failed to delete users.");
            }
        }
    };

    return (
        <div>
            <h2>{isRegister ? "Register" : "Login"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">{isRegister ? "Register" : "Login"}</button>
            </form>
            {onDeleteUsers && (
                <button onClick={handleDeleteUsers}>Delete All Users</button>
            )}
            {message && <p>{message}</p>}
        </div>
    );
};

export default AuthForm;

