import base64
import hashlib
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

# HTTP Bearer token extractor (Authorization: Bearer <token>)
security = HTTPBearer()

# JWT configuration
SECRET_KEY = "secret"          # Secret key used to sign JWTs (should come from env vars)
ALGORITHM = "HS256"             # JWT signing algorithm

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hashes a plaintext password securely.

    Steps:
    1. Hash password using SHA-256
    2. Base64-encode the hash
    3. Apply bcrypt hashing with salt
    """
    hashed = bcrypt.hashpw(
        base64.b64encode(
            hashlib.sha256(password.encode("utf-8")).digest()
        ),
        bcrypt.gensalt()
    ).decode("utf-8")

    return hashed


def verify_password(plain_password: str, hashed_password: str):
    """
    Verifies a plaintext password against a stored bcrypt hash.

    Steps:
    1. SHA-256 hash the input password
    2. Base64-encode the hash
    3. Compare with stored bcrypt hash
    """
    processed = base64.b64encode(
        hashlib.sha256(plain_password.encode("utf-8")).digest()
    )

    return bcrypt.checkpw(processed, hashed_password.encode("utf-8"))


def get_current_user(token=Depends(security)):
    """
    Extracts and validates the current user from JWT token.

    - Decodes JWT from Authorization header
    - Returns payload if token is valid
    - Raises 401 error if token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")