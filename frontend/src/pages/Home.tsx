import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Bienvenue dans Fiesta de los Muertos SaaS</h1>
      <p>Bienvenue dans le jeu collaboratif où les morts se souviennent... Serez-vous capable de deviner qui est qui ?</p>

      <div style={{ marginTop: '20px' }}>
        <Link to="/register">
          <button style={{ marginRight: '10px' }}>S'inscrire</button>
        </Link>
        
        <Link to="/play">
          <button>Jouer</button>
        </Link>
      </div>
    </div>
  );
};

export default Home;

