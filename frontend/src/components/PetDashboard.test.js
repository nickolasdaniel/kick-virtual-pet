// frontend/src/components/PetDashboard.test.js
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import PetDashboard from './PetDashboard';
import axios from 'axios';

jest.mock('axios');

describe('PetDashboard', () => {
  const initialPet = { id: 1, name: 'TestPet', hunger: 50, energy: 50, happiness: 50, health: 100, mood: 'neutral' };

  beforeEach(() => {
    // When the component mounts, it calls GET /api/pet/
    axios.get.mockResolvedValueOnce({ data: [initialPet] });
  });

  test('renders initial pet state', async () => {
    render(<PetDashboard />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/TestPet/i)).toBeInTheDocument());
  });

  test('sends command when Feed button clicked', async () => {
    render(<PetDashboard />);
    // Wait for initial pet info to load.
    await waitFor(() => expect(screen.getByText(/TestPet/i)).toBeInTheDocument());
    
    // Prepare the updated pet state after !feed command:
    const updatedPet = { ...initialPet, hunger: 40, energy: 60 };
    axios.post.mockResolvedValueOnce({ data: updatedPet });
    
    // Click the Feed button.
    fireEvent.click(screen.getByText(/Feed/i));
    
    // Wait for the updated state to be reflected in the UI.
    await waitFor(() => expect(screen.getByText(/Hunger:\s*40/i)).toBeInTheDocument());
  });
});
