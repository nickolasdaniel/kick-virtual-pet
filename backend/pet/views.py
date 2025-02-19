# backend/pet/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VirtualPet, Command
from .serializers import VirtualPetSerializer

class VirtualPetViewSet(viewsets.ModelViewSet):
    queryset = VirtualPet.objects.all()
    serializer_class = VirtualPetSerializer

class ProcessCommandView(APIView):
    """
    API endpoint to queue a chat command.
    """
    def post(self, request):
        command = request.data.get('command')
        if not command:
            return Response({"error": "Command not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Instead of processing immediately, create a Command entry.
            Command.objects.create(command_text=command)
            return Response({"status": "command queued"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
