// SkullCardHeader.tsx
import React from "react";

interface SkullCardProps {
    children: React.ReactNode;
}

const SkullCardHeader: React.FC<SkullCardProps> = ({ children }) => (
    <form>
        <div className="relative w-48 h-60 bg-white rounded-xl shadow-md p-4 flex flex-col items-center justify-between border-2 border-gray-800">
            <div className="w-full flex flex-col items-center relative">
                {/* Décorations supérieures */}
                <div className="absolute top-0 w-full flex justify-center">
                    <div className="w-10 h-2 bg-yellow-500 rounded-full mr-2"></div>
                    <div className="w-10 h-2 bg-red-500 rounded-full"></div>
                </div>
                {/* Yeux */}
                <div className="flex justify-between w-full mt-4">
                    <div className="w-10 h-10 bg-black rounded-full border-4 border-orange-500"></div>
                    <div className="w-10 h-10 bg-black rounded-full border-4 border-orange-500"></div>
                </div>
                {/* Nez */}
                <div className="w-4 h-6 bg-black rounded-b-full mt-2"></div>
                {/* Bouche */}
                <div className="mt-4 flex space-x-1">
                    <div className="w-3 h-3 bg-black rounded-full"></div>
                    <div className="w-3 h-3 bg-black rounded-full"></div>
                    <div className="w-3 h-3 bg-black rounded-full"></div>
                    <div className="w-3 h-3 bg-black rounded-full"></div>
                </div>
            </div>
            {children}
        </div>
    </form>
);

export default SkullCardHeader;
