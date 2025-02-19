import secrets

def generate_state(length=16):
    return secrets.token_urlsafe(length)

# Example usage:
state = generate_state()
print("State:", state)