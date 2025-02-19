import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PetDashboard = () => {
  const [pet, setPet] = useState(null);

  useEffect(() => {
    fetchPet();
  }, []);

  const fetchPet = async () => {
    try {
      const res = await axios.get('/api/pet/');
      setPet(res.data[0]);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCommand = async (command) => {
    try {
      // IMPORTANT: Use the response from POST to update state
      const res = await axios.post('/api/command/', { command });
      setPet(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (!pet) return <div>Loading...</div>;

  return (
    <div>
      <h2>{pet.name}</h2>
      <p>Hunger: {pet.hunger}</p>
      <p>Energy: {pet.energy}</p>
      <p>Happiness: {pet.happiness}</p>
      <p>Health: {pet.health}</p>
      <p>Mood: {pet.mood}</p>
      <div style={{ marginTop: '20px' }}>
        <button onClick={() => handleCommand('!feed')}>Feed</button>
        <button onClick={() => handleCommand('!play')}>Play</button>
        <button onClick={() => handleCommand('!clean')}>Clean</button>
        <button onClick={() => handleCommand('!medicate')}>Medicate</button>
        <button onClick={() => handleCommand('!evolve')}>Evolve</button>
      </div>
    </div>
  );
};

export default PetDashboard;
