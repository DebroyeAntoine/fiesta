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
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="w-full max-w-md bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-center mb-6">{isRegister ? "Register" : "Login"}</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-200"
            >
              {isRegister ? "Register" : "Login"}
            </button>
          </form>
          {onDeleteUsers && (
            <button
              onClick={handleDeleteUsers}
              className="mt-4 w-full bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition duration-200"
            >
              Delete All Users
            </button>
          )}
          {message && <p className="mt-4 text-center text-red-500">{message}</p>}
        </div>
      </div>
    );
};

export default AuthForm;

