# backend/pet/tasks.py
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import VirtualPet, Command
from .serializers import VirtualPetSerializer

@shared_task
def process_queued_commands():
    commands = Command.objects.all().order_by('timestamp')
    if not commands.exists():
        return "No commands to process."
    
    # Get or create the pet instance.
    pet = VirtualPet.objects.first()
    if not pet:
        pet = VirtualPet.objects.create()
    
    # Process each queued command.
    for cmd in commands:
        pet.apply_command(cmd.command_text)
    commands.delete()  # Clear the queue after processing.
    
    # Broadcast the updated pet state using Django Channels.
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "pet_updates",
        {
            "type": "pet_update",
            "data": VirtualPetSerializer(pet).data,
        }
    )
    return "Processed aggregated commands."
