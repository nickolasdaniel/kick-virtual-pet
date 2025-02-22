# kick_integration/kick_chat_listener.py
import os
import json
import requests
import websocket

# Load configuration from environment variables (or define them here)
KICK_CHAT_URL = os.environ.get("KICK_CHAT_URL", "wss://kick-chat.example.com")
# The backend endpoint to post commands to
BACKEND_COMMAND_ENDPOINT = os.environ.get("BACKEND_COMMAND_ENDPOINT", "http://localhost:8000/api/command/")

def on_message(ws, message):
    """Callback for received chat messages."""
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print("Received non-JSON message:", message)
        return

    # Assume the chat message is in a field called "message"
    chat_text = data.get("message", "")
    
    # Check if the message starts with '!' (indicating a command)
    if chat_text.startswith("!"):
        print(f"Received command: {chat_text}")
        # Forward the command to the backend API
        payload = {"command": chat_text}
        try:
            response = requests.post(BACKEND_COMMAND_ENDPOINT, json=payload)
            if response.status_code == 200:
                print(f"Command '{chat_text}' successfully posted (HTTP {response.status_code}).")
            else:
                print(f"Failed to post command '{chat_text}' (HTTP {response.status_code}).")
        except Exception as e:
            print(f"Error posting command '{chat_text}': {e}")

def on_error(ws, error):
    """Callback for errors."""
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    """Callback when connection closes."""
    print("WebSocket closed:", close_status_code, close_msg)

def on_open(ws):
    """Callback when connection opens."""
    print("WebSocket connection opened.")

def run_listener():
    websocket.enableTrace(True)
    ws_app = websocket.WebSocketApp(
        KICK_CHAT_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws_app.on_open = on_open
    ws_app.run_forever()

if __name__ == "__main__":
    run_listener()
