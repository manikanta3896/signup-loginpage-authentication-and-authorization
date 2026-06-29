from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Password Hashing Configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================
# Hash Password
# ==========================
def hash_password(password: str) -> str:
    """
    Convert plain password into hashed password.
    """
    return pwd_context.hash(password)


# ==========================
# Verify Password
# ==========================
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify entered password with hashed password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================
# Create JWT Access Token
# ==========================
def create_access_token(data: dict):
    """
    Generate JWT Token
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================
# Verify JWT Token
# ==========================
def verify_token(token: str):
    """
    Verify JWT Token and return username
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            return None

        return username

    except JWTError:
        return None