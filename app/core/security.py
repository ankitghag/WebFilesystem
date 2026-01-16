from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from app.core.config import setting
from jose import JWTError, jwt

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

from app.core.config import setting

def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create access JWT token - placeholder implementation
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "aud": setting.JWT_AUDIENCE,
        "iss": setting.JWT_ISSUER
    })

    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token=token,
            key=setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM],
            audience=setting.JWT_AUDIENCE,
            issuer=setting.JWT_ISSUER
        )            
        return payload
    except JWTError as err:
        print(f"JWT ERROR : {err}")
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """    
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password for storing.
    """
    return pwd_context.hash(password)
