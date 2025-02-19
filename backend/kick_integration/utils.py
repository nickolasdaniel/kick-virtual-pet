# backend/kick_integration/utils.py
import requests
from django.conf import settings

def get_kick_public_key():
    """
    Fetches the current Kick public key from the endpoint.
    Endpoint: /public/v1/public-key
    """
    url = f"https://kick.com/public/v1/public-key"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Assume the key is in the 'public_key' field (adjust based on actual response)
        public_key = data.get("public_key")
        if not public_key:
            raise ValueError("Public key not found in response")
        return public_key
    except Exception as e:
        # Log the error or handle it as needed
        raise RuntimeError("Failed to retrieve Kick public key") from e
