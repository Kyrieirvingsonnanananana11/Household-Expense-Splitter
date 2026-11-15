"""Password hashing and authentication helpers (standard library only)."""
import hashlib
import hmac
import secrets

ITERATIONS = 300_000

def make_password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), ITERATIONS)
    return digest.hex(), salt

def verify_password(password, stored_hash, salt):
    candidate, _ = make_password_hash(password, salt)
    return hmac.compare_digest(candidate, stored_hash)
