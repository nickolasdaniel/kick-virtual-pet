import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const PetDashboard = () => {
  const [pet, setPet] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const ws = new WebSocket(`${protocol}://localhost:8000/ws/pet/`);
    wsRef.current = ws;
    
    ws.onopen = () => {
      console.log("WebSocket connection established");
    };
    
    ws.onmessage = (event) => {
      console.log("Received WebSocket message:", event.data);
      const updatedPet = JSON.parse(event.data);
      setPet(updatedPet);
      setIsUpdating(false);
    };
    
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
    
    ws.onclose = (e) => {
      console.warn("WebSocket closed:", e);
    };
    
    return () => {
      ws.close();
    };
  }, []);

  const fetchPet = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/pet/');
      setPet(res.data[0]);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPet();
  }, []);

  const handleCommand = async (command) => {
    try {
      setIsUpdating(true);
      await axios.post('http://localhost:8000/api/command/', { command });
      // Do not update state here; wait for the WebSocket update.
    } catch (err) {
      console.error(err);
      setIsUpdating(false);
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
      {isUpdating && <p style={{ color: "gray" }}>Processing command...</p>}
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
