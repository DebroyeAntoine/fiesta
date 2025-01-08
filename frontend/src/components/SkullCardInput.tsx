import React, { useState, useEffect } from "react";
import SkullCardBase from "./SkullCardBase";

interface SkullCardInputProps {
    word: string;
    setWord: (value: string) => void;
    handleValidate: () => void;
    isNewRound: boolean;
}

const SkullCardInput: React.FC<SkullCardInputProps> = ({
    word,
    setWord,
    handleValidate,
    isNewRound,
}) => {
    const [isButtonDisabled, setIsButtonDisabled] = useState(false);

    const handleClick = () => {
        setIsButtonDisabled(true);
        handleValidate();
    };

    useEffect(() => {
        setIsButtonDisabled(false);
    }, [isNewRound]);

    return (
        <SkullCardBase>
            <div className="w-full p-2 mt-4 bg-gray-200 rounded-lg flex justify-center items-center">
                <input
                    type="text"
                    value={word}
                    onChange={(e) => setWord(e.target.value)}
                    className="bg-transparent border-none text-center text-xl font-bold outline-none"
                    placeholder="Type here"
                />
            </div>
            <button
                onClick={handleClick}
                disabled={isButtonDisabled}
                className={`mt-4 py-2 px-4 rounded transition duration-300 ease-in-out ${
                    isButtonDisabled
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-secondary hover:bg-primary text-white font-semibold"
                }`}
            >
                Valider
            </button>
        </SkullCardBase>
    );
};

export default SkullCardInput;
