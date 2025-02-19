# kick_virtual_pet/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pet.urls')),
    path('api/kick/', include('kick_integration.urls')),
]
