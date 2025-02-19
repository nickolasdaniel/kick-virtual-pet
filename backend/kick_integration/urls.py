# backend/kick_integration/urls.py
from django.urls import path
from .views import kick_oauth_start, kick_oauth_callback, kick_webhook

urlpatterns = [
    path('oauth/start/', kick_oauth_start, name='kick-oauth-start'),
    path('oauth/callback/', kick_oauth_callback, name='kick-oauth-callback'),
    path('webhook/', kick_webhook, name='kick-webhook'),
]
