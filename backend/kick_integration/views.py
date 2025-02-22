import json
import hmac
import hashlib
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)

def load_public_key():
    """
    In test mode, use the hardcoded test public key.
    Otherwise, you might implement retrieval and caching.
    """
    public_key_pem = settings.KICK_PUBLIC_KEY
    try:
        return serialization.load_pem_public_key(public_key_pem.encode())
    except Exception as e:
        logger.exception("Failed to load public key")
        raise

@csrf_exempt
def kick_webhook(request):
    logger.info("Received webhook request")
    body = request.body

    # In test mode, optionally bypass signature verification
    if not settings.KICK_TEST_MODE:
        signature = request.headers.get('X-Kick-Signature')
        if not signature:
            logger.error("Missing signature")
            return HttpResponseBadRequest("Missing signature")
    
        try:
            signature_bytes = bytes.fromhex(signature)
        except ValueError:
            logger.exception("Invalid signature format")
            return HttpResponseBadRequest("Invalid signature format")
    
        try:
            public_key = load_public_key()
            public_key.verify(
                signature_bytes,
                body,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        except Exception as e:
            logger.exception("Signature verification failed")
            return HttpResponseBadRequest("Signature verification failed")
    else:
        logger.info("Test mode enabled, skipping signature verification")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        logger.exception("Invalid JSON")
        return HttpResponseBadRequest("Invalid JSON")

    # Process the payload
    if payload.get("event_type") == "chat_message":
        message = payload.get("data", {}).get("message", "")
        logger.info(f"Received chat message: {message}")
        if message.startswith("!"):
            # Forward the command to your backend command endpoint
            import requests
            command_payload = {"command": message}
            try:
                response = requests.post(settings.BACKEND_COMMAND_ENDPOINT, json=command_payload)
                logger.info(f"Posted command: {message}, response: {response.status_code}")
            except Exception as e:
                logger.exception("Failed to post command")
                return HttpResponse("Failed to post command", status=500)

    return JsonResponse({"status": "received"})

def kick_oauth_start(request):
    # Placeholder implementation
    return HttpResponse("kick_oauth_start endpoint placeholder. Redirect user to Kick's OAuth authorization page here.")

def kick_oauth_callback(request):
    # Placeholder implementation
    code = request.GET.get("code")
    if not code:
        return HttpResponseBadRequest("Missing code")
    return HttpResponse(f"kick_oauth_callback received code: {code}")