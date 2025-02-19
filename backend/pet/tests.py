# backend/pet/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pet.models import VirtualPet, Command
from pet.tasks import process_queued_commands

##########################################
# Model Tests: Directly test apply_command
##########################################

class VirtualPetModelTest(TestCase):
    def setUp(self):
        # Initial state for tests; adjust values as needed.
        self.pet = VirtualPet.objects.create(
            name="TestPet", hunger=50, energy=50, happiness=50, health=80, mood="neutral"
        )

    def test_apply_feed_command(self):
        self.pet.apply_command("!feed")
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.hunger, 40)   # 50 - 10
        self.assertEqual(self.pet.energy, 60)   # 50 + 10

    def test_apply_play_command(self):
        self.pet.apply_command("!play")
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.happiness, 60)  # 50 + 10
        self.assertEqual(self.pet.energy, 45)     # 50 - 5

    def test_apply_clean_command(self):
        self.pet.apply_command("!clean")
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.health, 90)  # 80 + 10, capped at 100 if needed
        self.assertEqual(self.pet.mood, "happy")

    def test_apply_medicate_command(self):
        self.pet.apply_command("!medicate")
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.health, 100)  # 80 + 20, but not above 100
        self.assertEqual(self.pet.mood, "relieved")

    def test_apply_evolve_command_success(self):
        # Set up conditions to allow evolution.
        self.pet.happiness = 70
        self.pet.energy = 70
        self.pet.save()
        self.pet.apply_command("!evolve")
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.mood, "evolved")

    def test_apply_evolve_command_fail(self):
        # Conditions not met: no evolution should occur.
        self.pet.happiness = 60
        self.pet.energy = 60
        self.pet.save()
        self.pet.apply_command("!evolve")
        self.pet.refresh_from_db()
        self.assertNotEqual(self.pet.mood, "evolved")


##########################################
# API Endpoint Tests: Testing /api/command/ endpoint
##########################################

class VirtualPetAPITest(APITestCase):
    def setUp(self):
        self.pet = VirtualPet.objects.create(
            name="TestPet", hunger=50, energy=50, happiness=50, health=80, mood="neutral"
        )

    def test_get_pet_list(self):
        url = reverse('virtualpet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data[0])

    def test_post_feed_command(self):
        url = reverse('process-command')
        data = {"command": "!feed"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()  # Process the queued command(s)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.hunger, 40)
        self.assertEqual(self.pet.energy, 60)

    def test_post_play_command(self):
        url = reverse('process-command')
        data = {"command": "!play"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.happiness, 60)
        self.assertEqual(self.pet.energy, 45)

    def test_post_clean_command(self):
        url = reverse('process-command')
        data = {"command": "!clean"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.health, 90)
        self.assertEqual(self.pet.mood, "happy")

    def test_post_medicate_command(self):
        url = reverse('process-command')
        data = {"command": "!medicate"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.health, 100)
        self.assertEqual(self.pet.mood, "relieved")

    def test_post_evolve_command_success(self):
        # Set conditions for evolution.
        self.pet.happiness = 70
        self.pet.energy = 70
        self.pet.save()
        url = reverse('process-command')
        data = {"command": "!evolve"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.mood, "evolved")

    def test_post_evolve_command_fail(self):
        # Conditions not met: evolution should not happen.
        self.pet.happiness = 60
        self.pet.energy = 60
        self.pet.save()
        url = reverse('process-command')
        data = {"command": "!evolve"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Command.objects.count(), 1)
        process_queued_commands()
        self.pet.refresh_from_db()
        self.assertNotEqual(self.pet.mood, "evolved")
