import hashlib
import binascii
import os
import secrets

def hash_password(password: str) -> tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        tuple[str, str]: A tuple containing the hex-encoded salt and the hex-encoded hash.
    """
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return binascii.hexlify(salt).decode('ascii'), binascii.hexlify(pwd_hash).decode('ascii')

def verify_password(stored_salt: str, stored_hash: str, provided_password: str) -> bool:
    """
    Verifies a password against a stored salt and hash.

    Args:
        stored_salt (str): The hex-encoded salt string.
        stored_hash (str): The hex-encoded hash string.
        provided_password (str): The plaintext password to verify.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        salt = binascii.unhexlify(stored_salt)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return secrets.compare_digest(binascii.hexlify(pwd_hash).decode('ascii'), stored_hash)
    except (ValueError, TypeError):
        return False
