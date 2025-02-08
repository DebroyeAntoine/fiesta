import React from "react";
import AuthForm from "./AuthForm";
import { useNavigate } from "react-router-dom";

const Register: React.FC = () => {
    const navigate = useNavigate();
    const handleRegister = async (username: string, password: string) => {
        const response = await fetch("/auth_api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error("Failed to register");
        } else {
            console.log(data);
            console.log(data.token);
            localStorage.setItem("token", data.token);
            navigate("/gameList");
            //navigate(`/game/${data.gameId}`);
        }
    };

    const handleDeleteUsers = async () => {
        const response = await fetch("/delete", {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("Failed to delete users");
        }
    };

    return (
        <AuthForm
            onSubmit={handleRegister}
            onDeleteUsers={handleDeleteUsers}
            isRegister={true}
        />
    );
};

export default Register;
