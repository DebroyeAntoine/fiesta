import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import SkullBackground from "../assets/Skull.svg";

const SugarSkull = () => <img src={SkullBackground} alt="Sugar Skull" />;
const Home = () => {
    return (
        <div className="min-h-screen bg-gradient-to-b from-purple-900 via-purple-800 to-orange-700 text-white p-8">
            <div className="absolute inset-0 flex items-center justify-center w-full h-full opacity-20 pointer-events-none">
                <div className="max-w-[400px] max-h-[400px] w-full h-full">
                    <SugarSkull />
                </div>
            </div>
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="max-w-4xl mx-auto text-center"
            >
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{
                        type: "spring",
                        stiffness: 260,
                        damping: 20,
                        duration: 1.5,
                    }}
                ></motion.div>

                <motion.h1
                    className="text-6xl font-bold mb-6 text-orange-400"
                    animate={{ scale: [1, 1.02, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                >
                    Fiesta de los Muertos
                </motion.h1>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mb-12 text-xl"
                >
                    <p className="mb-4">
                        Bienvenue dans un monde où les morts se souviennent...
                    </p>
                    <p className="text-orange-300">
                        Serez-vous capable de deviner qui est qui ?
                    </p>
                </motion.div>

                <motion.div
                    className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-lg mx-auto"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                >
                    <Link to="/register">
                        <motion.button
                            className="w-full px-8 py-4 bg-orange-500 rounded-lg text-lg font-semibold hover:bg-orange-400 transition-colors"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Rejoindre la fête
                        </motion.button>
                    </Link>

                    <Link to="/login">
                        <motion.button
                            className="w-full px-8 py-4 bg-purple-600 rounded-lg text-lg font-semibold hover:bg-purple-500 transition-colors"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Se connecter
                        </motion.button>
                    </Link>
                </motion.div>

                <motion.div
                    className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.2 }}
                >
                    <div className="bg-purple-800 bg-opacity-50 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2">
                            Jeu Collaboratif
                        </h3>
                        <p>
                            Jouez avec vos amis dans une expérience unique et
                            mystérieuse
                        </p>
                    </div>

                    <div className="bg-purple-800 bg-opacity-50 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2">Mystère</h3>
                        <p>
                            Découvrez les secrets cachés derrière chaque
                            personnage
                        </p>
                    </div>

                    <div className="bg-purple-800 bg-opacity-50 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2">Festivités</h3>
                        <p>
                            Plongez dans l'ambiance colorée du Dia de los
                            Muertos
                        </p>
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
};

export default Home;
