# backend/pet/management/commands/process_commands.py
from django.core.management.base import BaseCommand
from pet.models import VirtualPet, Command
from pet.serializers import VirtualPetSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ProcessCommandsCommand(BaseCommand):
    help = "Process and aggregate queued pet commands"

    def handle(self, *args, **options):
        # Retrieve all queued commands, ordered by timestamp.
        commands = Command.objects.all().order_by('timestamp')
        if not commands.exists():
            self.stdout.write("No commands to process.")
            return

        # Get the pet instance (create if necessary)
        pet = VirtualPet.objects.first()
        if not pet:
            pet = VirtualPet.objects.create()

        # Process each command sequentially.
        for cmd in commands:
            pet.apply_command(cmd.command_text)
        # Clear the command queue after processing.
        commands.delete()

        # Broadcast the updated pet state using Channels.
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "pet_updates",
            {
                "type": "pet_update",
                "data": VirtualPetSerializer(pet).data,
            }
        )
        self.stdout.write("Processed aggregated commands.")
