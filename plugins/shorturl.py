import os
import hmac
import hashlib
from config import SHORT_API, SHORT_URL

SECRET_KEY = b"VERCEL_TUNNEL_SECURE_KEY_2026"

def get_short(url):
    """
    Encrypts the Vercel proxy tunnel URL inside Telegram so no one can
    decode or bypass it without going through the official Chrome verification.
    """
    raw_data = f"{SHORT_URL}|{SHORT_API}|{url}".encode("utf-8")
    iv = os.urandom(8)
    
    keystream = b""
    counter = 0
    while len(keystream) < len(raw_data):
        block = hashlib.sha256(SECRET_KEY + iv + str(counter).encode()).digest()
        keystream += block
        counter += 1
        
    encrypted = bytes(a ^ b for a, b in zip(raw_data, keystream[:len(raw_data)]))
    sig = hmac.new(SECRET_KEY, iv + encrypted, hashlib.sha256).hexdigest()[:16]
    
    return f"cipher://{iv.hex()}.{encrypted.hex()}.{sig}"
