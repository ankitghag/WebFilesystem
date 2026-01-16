import os
import secrets
from dotenv import load_dotenv
load_dotenv(override=True)
class csetting():
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    SQLALCHEMY_DATABASE_URI= os.getenv("USERDATABASE_URL", None)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "*")
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "http://localhost:8000")

setting= csetting()