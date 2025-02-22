from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from pet.models import Command, VirtualPet
from pet.serializers import VirtualPetSerializer

class VirtualPetViewSet(viewsets.ModelViewSet):
    queryset = VirtualPet.objects.all()
    serializer_class = VirtualPetSerializer

class ProcessCommandView(APIView):
    def post(self, request):
        command = request.data.get('command')
        if not command:
            return Response({"error": "Command not provided"}, status=status.HTTP_400_BAD_REQUEST)
        # Queue the command (the Celery task will process it later)
        Command.objects.create(command_text=command)
        return Response({"status": "command queued"}, status=status.HTTP_200_OK)
