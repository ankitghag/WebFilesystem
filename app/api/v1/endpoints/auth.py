from fastapi import APIRouter, Depends,  status, Request
from app.dtos.custom_response import CustomResponse
from app.schemas.sch_user import UserCreate, UserResponse, UserLogin
from app.dependencies.dp_services import get_user_service
from app.services.user_service import UserService
from app.utils.response import create_response
from app.exceptions.http_exceptions import BadRequestError, UnauthorizedError
from app.models.app_model import UserRole
from app.core.security import verify_password, create_access_token
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
    else:
        user_in.role= UserRole.USER.value
        res= await dbcon.user_create(user_in)
    return create_response(
    data=UserResponse.from_orm(res),
    message="User created successfully",
    status_code=status.HTTP_201_CREATED)


@router.post("/signin", response_model=CustomResponse[UserResponse], summary= "Sign In", description= "SignIn") 
async def login(user:UserLogin, dbcon:UserService=Depends(get_user_service)):
    retuser= await dbcon.get_user_by_email(user.email)
    res= None
    if not retuser and not verify_password(user.password,retuser.password_hash ):
        raise UnauthorizedError(detail="Invalid Credential", error_code= "UNAUTHORIZED")

    user_dict= {"email": user.email, "username" : retuser.username, "userid": retuser.id}
    create_token= create_access_token(data= user_dict)
    return create_response(data= create_token, message="User Logged In", status_code=status.HTTP_200_OK)

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