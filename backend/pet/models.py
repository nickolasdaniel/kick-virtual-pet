# backend/pet/models.py
from django.db import models

class VirtualPet(models.Model):
    name = models.CharField(max_length=100, default='KickPet')
    hunger = models.IntegerField(default=50)
    energy = models.IntegerField(default=50)
    happiness = models.IntegerField(default=50)
    health = models.IntegerField(default=100)
    mood = models.CharField(max_length=50, default='neutral')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def apply_command(self, command: str):
        """
        Update pet state based on the incoming command.
        """
        if command == '!feed':
            # Feeding reduces hunger and boosts energy.
            self.hunger = max(self.hunger - 10, 0)
            self.energy = min(self.energy + 10, 100)
        elif command == '!play':
            # Playing increases happiness and reduces energy.
            self.happiness = min(self.happiness + 10, 100)
            self.energy = max(self.energy - 5, 0)
        elif command == '!clean':
            # Cleaning improves health and mood.
            self.health = min(self.health + 10, 100)
            self.mood = "happy"
        elif command == '!medicate':
            # Medication improves health more significantly.
            self.health = min(self.health + 20, 100)
            self.mood = "relieved"
        elif command == '!evolve':
            # Evolve only if pet has sufficient happiness and energy.
            if self.happiness >= 70 and self.energy >= 70:
                self.mood = "evolved"
                # You can add additional state changes (e.g., flag for new appearance)
        self.save()
        return self

# New model to queue incoming commands.
class Command(models.Model):
    command_text = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.command_text
