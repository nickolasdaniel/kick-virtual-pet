// frontend/src/App.test.js
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';

// We need to mock axios.get in App as well.
jest.mock('axios');

test('renders pet dashboard with pet name', async () => {
  const petData = { id: 1, name: 'TestPet', hunger: 50, energy: 50, happiness: 50, health: 100, mood: 'neutral' };
  axios.get.mockResolvedValueOnce({ data: [petData] });

  render(<App />);
  // Initially it shows "Loading...", then eventually the pet name should appear.
  await waitFor(() => expect(screen.getByText(/TestPet/i)).toBeInTheDocument());
});
