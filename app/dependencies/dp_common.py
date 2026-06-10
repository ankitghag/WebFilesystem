from fastapi import Depends, Form, Request
from app.core.security import verify_token
from jose import JWTError, jwt
from app.exceptions.http_exceptions import InvalidJwtToken
from fastapi.security import OAuth2PasswordBearer
from app.schemas.sch_user import CreateNode

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def verify_jwt(token: str= Depends(oauth2_scheme), isrefresh= False):
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
        if payload is None:
            if isrefresh:
                raise InvalidJwtToken("Invalid refresh token", "INVALID_REFRESH_TOKEN")
            else:
                raise InvalidJwtToken("Invalid token", "INVALID_TOKEN")

        return payload  # or return user_id

    except JWTError:
        print('JWTERROR - TOKEN INVALID OR EXPRIED')
        raise InvalidJwtToken(
            error_code= "Invalid JWT Token",
            detail="Token is invalid or expired"
        )

def verify_ref_jwt(request: Request):
    reftoken= request.cookies.get("refresh_token")
    print(f" REFTOKEN : {reftoken}")
    if not reftoken:
        raise InvalidJwtToken("Refresh token missing", "REFRESH_TOKEN_MISSING")
    else:
        payload= verify_jwt(reftoken, True)
        return payload




   


# class FileMeta(BaseModel):
#     parent_id: int
#     description: str | None = None

#     @classmethod
#     def as_form(
#         cls,
#         parent_id: int = Form(...),
#         description: str | None = Form(None),
#     ):
#         return cls(
#             parent_id=parent_id,
#             description=description,
#         )
def get_create_node_form(nodename:str= Form(...), pid:int= Form(...), ppath:str= Form(...)):
    return CreateNode(nodename= nodename, pid= pid, ppath= ppath)
