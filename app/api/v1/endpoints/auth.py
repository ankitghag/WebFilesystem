from fastapi import APIRouter, Depends,  status, Request, Response
from app.dtos.custom_response import CustomResponse
from app.schemas.sch_user import UserCreate, UserResponse, UserLogin
from app.dependencies.dp_services import get_user_service, get_token_service
from app.dependencies.dp_common import verify_ref_jwt
from app.services.user_service import UserService
from app.utils.response import create_response
from app.exceptions.http_exceptions import BadRequestError, UnauthorizedError, InvalidRole
from app.models.app_model import UserRole
from app.core.security import verify_password, create_access_token, create_refresh_token
#
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

router= APIRouter()

@router.get("/")
def testuser():
    return "USER TESTED"

@router.post("/signup",
response_model=CustomResponse[UserResponse],
summary="Sign UP",
description="SignUp User"
)
async def usersignup(user_in:UserCreate,dbcon:UserService=Depends(get_user_service)):
    chk_user_exists= await dbcon.get_user_by_email(user_in.email)
    res= None
    if chk_user_exists:
        raise BadRequestError(error_code="USER_ALREADY__EXISTS", detail="User with this emial already exists")
    elif user_in.role.upper() not in UserRole.__members__: 
        raise InvalidRole()
    else:
        user_in.role= UserRole[user_in.role.upper()]
        res= await dbcon.user_create(user_in)
    return create_response(
    data=UserResponse.from_orm(res),
    message="User created successfully",
    status_code=status.HTTP_201_CREATED)


@router.post("/signin", response_model=CustomResponse[UserResponse], summary= "Sign In", description= "SignIn") 
async def login(user:UserLogin,response: Response, dbcon:UserService=Depends(get_user_service),  tokdbcon= Depends(get_token_service)):
    retuser= await dbcon.get_user_by_email(user.email)
    res= None
    if not retuser and not verify_password(user.password,retuser.password_hash ):
        raise UnauthorizedError(detail="Invalid Credential", error_code= "UNAUTHORIZED")

    user_dict= {"email": user.email, "username" : retuser.username, "userid": retuser.id}
    access_token= create_access_token(data= user_dict)
    refresh_token= create_refresh_token(data= user_dict)
    reftok= await tokdbcon.create_ref_token(data= user_dict, rtok=refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  
        samesite="Lax"   # or "Strict"/"None"
    )
    rtres= create_response(data= access_token, message="User Logged In", status_code=status.HTTP_200_OK)
    rtres.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  
        samesite="Lax"   # or "Strict"/"None"
    )
    return rtres

@router.post("/xxsignin", response_model=CustomResponse[UserResponse], summary= "Sign In", description= "SignIn") 
async def login(request: Request, user: OAuth2PasswordRequestForm = Depends(), dbcon:UserService=Depends(get_user_service)):
    email, password = "", ""
    if user and user.username:
        email = user.username
        password = user.password
    else:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")
    retuser= await dbcon.get_user_by_email(email)
    res= None
    if not retuser and not verify_password(password,retuser.password_hash ):
        raise UnauthorizedError(detail="Invalid Credential", error_code= "UNAUTHORIZED")

    user_dict= {"email": email, "username" : retuser.username}
    create_token= create_access_token(data= user_dict)
    return create_response(data= create_token, message="User Logged In", status_code=status.HTTP_200_OK)


@router.post("/refresh", response_model=CustomResponse[UserResponse], summary= "refresh", description= "Refresh") 
async def refresh_token(request: Request, response: Response, payload= Depends(verify_ref_jwt), tokdbcon= Depends(get_token_service)):
    refresh_token = request.cookies.get("refresh_token")
    print(f"REFPAYLOAD : {payload}")

    user_dict= {"email": payload["email"], "username" : payload["username"], "userid": payload["userid"]}
    new_access_token= create_access_token(data= user_dict)
    new_refresh_token= create_refresh_token(data= user_dict)
    print(f"NEW TOKENS {new_access_token}")
    tokres= await tokdbcon.new_ref_token(user_dict["userid"],refresh_token, new_refresh_token)
    print(f"REFRESHi0 {tokres}")
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,  
        samesite="Lax"   # or "Strict"/"None"
    )
    print(f"REFRESHi2 {tokres}")
    # return {"access_token": new_access_token}
    rtres= create_response(data= new_access_token, message="Refresh TOKEN SUCCESS", status_code=status.HTTP_200_OK)
    rtres.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,  
        samesite="Lax"   # or "Strict"/"None"
    )
    print(rtres.body)
    return rtres


    