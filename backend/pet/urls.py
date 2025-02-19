# backend/pet/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualPetViewSet, ProcessCommandView

router = DefaultRouter()
router.register(r'pet', VirtualPetViewSet, basename='virtualpet')

urlpatterns = [
    path('', include(router.urls)),
    path('command/', ProcessCommandView.as_view(), name='process-command'),
]
