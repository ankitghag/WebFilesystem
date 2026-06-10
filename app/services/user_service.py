from typing import List, Optional, Union

#from app.core.security import get_password_hash
from app.models.app_model import User
from app.repositories.user_query import UserRepository
from app.schemas.sch_user import UserCreate, UserUpdate
from app.dtos.fs_node_dto import CreateGrpCmd
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.exceptions.http_exceptions import UserNotExsits, NotanAdmin

class UserService:    
    def __init__(self, db: AsyncSession, user_repo: UserRepository):
        """Initialize with user repository"""
        self.db = db
        self.user_repo = user_repo

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        result = await self.user_repo.get_user_by_email(email)
        return result

    async def user_create(self, user:UserCreate) -> User:
        user_dict= user.dict()
        print(f"USERDICt : {user_dict}")
        if "password" in user_dict:
            user_dict["password_hash"]= get_password_hash(user_dict["password"])
            del user_dict["password"]
        result= await self.user_repo.insert_data(user_dict)
        return result



