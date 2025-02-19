# backend/kick_integration/views.py
import os, requests, json, hmac, hashlib
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Endpoint to initiate OAuth flow.
def kick_oauth_start(request):
    client_id = settings.KICK_CLIENT_ID
    redirect_uri = settings.KICK_REDIRECT_URI
    scope = "chat:read users:read"  # adjust scopes as needed
    auth_url = (
        f"https://kick.com/oauth/authorize?client_id={client_id}"
        f"&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
    )
    return redirect(auth_url)

# Endpoint to handle OAuth callback.
def kick_oauth_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponseBadRequest("No code provided")

    token_url = "https://kick.com/oauth/token"
    data = {
        "client_id": settings.KICK_CLIENT_ID,
        "client_secret": settings.KICK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.KICK_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        # You might want to store the token (and refresh token) in your database
        return JsonResponse(token_data)
    else:
        return HttpResponseBadRequest("Token exchange failed")
    
@csrf_exempt
def kick_webhook(request):
    # Retrieve Kick signature from headers
    signature = request.headers.get('X-Kick-Signature')
    body = request.body

    # Verify the signature using the public key from Kick
    if signature:
        computed = hmac.new(
            settings.KICK_PUBLIC_KEY.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, computed):
            return HttpResponse("Invalid signature", status=400)

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    # Check if this is a chat message event
    if payload.get("event_type") == "chat_message":
        message = payload.get("data", {}).get("message", "")
        # If the message is a command, forward it to our command endpoint.
        if message.startswith("!"):
            # You can use requests to post to the command endpoint, or
            # you could call the backend logic directly.
            command_payload = {"command": message}
            requests.post(settings.BACKEND_COMMAND_ENDPOINT, json=command_payload)
    return HttpResponse("Received", status=200)
