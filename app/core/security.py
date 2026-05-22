"""
Security utilities and helpers
"""
import hashlib

def hash_api_key(key: str) -> str:
    """Generate SHA-256 hash of API key"""
    return hashlib.sha256(key.encode()).hexdigest()
