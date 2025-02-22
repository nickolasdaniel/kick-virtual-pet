from django.urls import re_path
from pet.consumers import PetConsumer

websocket_urlpatterns = [
    re_path(r'^ws/pet/$', PetConsumer.as_asgi()),
]