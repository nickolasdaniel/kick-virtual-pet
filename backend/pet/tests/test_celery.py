# backend/pet/tests/test_celery.py
from django.test import TestCase
from pet.models import VirtualPet, Command
from pet.tasks import process_queued_commands

class CeleryTaskTest(TestCase):
    def setUp(self):
        # Create a pet with initial stats.
        self.pet = VirtualPet.objects.create(
            name="TestPet",
            hunger=50,
            energy=50,
            happiness=50,
            health=80,
            mood="neutral"
        )
        # Queue one command for each type.
        Command.objects.create(command_text="!feed")
        Command.objects.create(command_text="!play")
        Command.objects.create(command_text="!clean")
        Command.objects.create(command_text="!medicate")
        # For evolve, we set up the pet so it qualifies.
        self.pet.happiness = 70
        self.pet.energy = 70
        self.pet.save()
        Command.objects.create(command_text="!evolve")

    def test_process_queued_commands(self):
        # Process all queued commands.
        result = process_queued_commands()
        self.assertEqual(result, "Processed aggregated commands.")
        
        # Refresh pet from the database.
        self.pet.refresh_from_db()
        
        # Expected updates:
        # !feed: hunger 50 -> 40, energy 50 -> 60
        # !play: happiness 50 -> 60, energy 60 -> 55 (60 - 5)
        # !clean: health 80 -> 90, mood becomes "happy"
        # !medicate: health 90 -> 100, mood becomes "relieved"
        # !evolve: Conditions met so mood becomes "evolved"
        #
        # Note: The commands are processed sequentially.
        # Final expected stats:
        self.assertEqual(self.pet.hunger, 40)
        self.assertEqual(self.pet.energy, 55)
        self.assertEqual(self.pet.happiness, 60)
        self.assertEqual(self.pet.health, 100)
        self.assertEqual(self.pet.mood, "evolved")
        
        # Verify the command queue is empty.
        self.assertEqual(Command.objects.count(), 0)
