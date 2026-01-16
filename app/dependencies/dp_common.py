from fastapi import Depends
from app.core.security import verify_token
from jose import JWTError, jwt
from app.exceptions.http_exceptions import InvalidJwtToken
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def verify_jwt(token: str= Depends(oauth2_scheme)):
    try:
        print(f"TOKEN :{token}")
        payload= verify_token(token)
        print(payload)


        # user_id: str = payload.get("sub")

        # if user_id is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid token"
        #     )

        return payload  # or return user_id

    except JWTError:
        raise InvalidJwtToken(
            error_code= "Invalid JWT Token",
            detail="Token is invalid or expired"
        )
