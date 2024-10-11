import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Appel à l'API Flask (point d'entrée racine)
      fetch('http://127.0.0.1:5000')
      .then((res) => res.json())  // Parse la réponse en JSON
      .then((data) => { console.log(data); setMessage(data.message);})  // Affiche la valeur du champ 'message'
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Fiesta de los Muertos SaaS</h1>
        <p>Message from Flask: {message}</p>
      </header>
    </div>
  );
}

export default App;

