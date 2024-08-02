from cryptography.fernet import Fernet
import os
import base64


# Generate a key for encryption and decryption
# You should do this once and store the key securely, e.g., in an environment variable or a secure vault
def generate_key():
    return Fernet.generate_key()


# Load your secret key (this should be securely stored and retrieved)
secret_key = os.environ.get('WALLET_SECRET_KEY', base64.urlsafe_b64encode(os.urandom(32)))  # Example of loading from env

# Initialize the Fernet class
cipher_suite = Fernet(secret_key)


def encrypt_data(data: str) -> str:
    """Encrypts the data."""
    if not data:
        return None
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts the data."""
    if not encrypted_data:
        return None
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
