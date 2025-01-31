// SocketContext.tsx
import React, { createContext, useContext, useEffect } from "react";
import { io, Socket } from "socket.io-client";

const SocketContext = createContext<Socket | null>(null);

export const SocketProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const socket = io("http://localhost:5000", { transports: ["websocket"] });

    useEffect(() => {
        socket.on("connect", () => {
            console.log("Connecté au serveur Socket.IO avec l'ID :", socket.id);
            socket.emit("join_room", { token: localStorage.getItem("token") });
        });

        socket.on("disconnect", (reason) => {
            console.log("Déconnecté du serveur Socket.IO :", reason);
        });

        socket.on("reconnect", (attemptNumber) => {
            console.log(
                "Reconnecté au serveur Socket.IO après",
                attemptNumber,
                "tentatives"
            );
        });

        return () => {
            socket.disconnect();
        };
    }, [socket]);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};

export const useSocket = () => {
    const context = useContext(SocketContext);
    if (!context) {
        throw new Error("useSocket doit être utilisé dans un SocketProvider");
    }
    return context;
};
