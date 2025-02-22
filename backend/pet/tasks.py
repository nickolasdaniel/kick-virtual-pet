from celery import shared_task
from pet.models import VirtualPet, Command
from pet.serializers import VirtualPetSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def process_queued_commands():
    commands = Command.objects.all().order_by('timestamp')
    if not commands.exists():
        return "No commands to process."
    
    pet = VirtualPet.objects.first()
    if not pet:
        pet = VirtualPet.objects.create()
    
    for cmd in commands:
        pet.apply_command(cmd.command_text)
    commands.delete()  # Clear the command queue
    
    # Broadcast updated pet state via Channels
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "pet_updates",
        {
            "type": "pet_update",
            "data": VirtualPetSerializer(pet).data,
        }
    )
    return "Processed aggregated commands."
