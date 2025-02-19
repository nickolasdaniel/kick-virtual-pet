from rest_framework import serializers
from .models import VirtualPet

class VirtualPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPet
        fields = '__all__'