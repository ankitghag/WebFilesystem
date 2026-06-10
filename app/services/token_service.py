from typing import List, Optional, Union

#from app.core.security import get_password_hash
from app.models.app_model import User
from app.repositories.token_query import TokenRepository
from app.schemas.sch_user import UserCreate, UserUpdate
from app.dtos.fs_node_dto import CreateGrpCmd
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.exceptions.http_exceptions import UserNotExsits, NotanAdmin, InvalidJwtToken
from datetime import datetime, timedelta


class TokenService:    
    def __init__(self, db: AsyncSession, token_repo: TokenRepository):
        """Initialize with user repository"""
        self.db = db
        self.token_repo = token_repo

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        result = await self.user_repo.get_user_by_email(email)
        return result

    async def create_ref_token(self, data, rtok):
        reftok= {"user_id":data["userid"], "token": rtok, "expires_at": datetime.now() + timedelta(days=7)}
        refobj= await self.token_repo.insert_data(reftok)
        return {"id": refobj.id, "userid": refobj.user_id}


    async def new_ref_token(self, userid, reftoken, newreftoken):
        res= None
        async with self.db.begin():
            rtok= await self.token_repo.get_ref_token(reftoken, False)
            print(f"RTOK : {rtok}")
            if not rtok or rtok[0].is_revoked:
                raise InvalidJwtToken("Invalid irefresh token", "INVALID_TOKEN")
            robj= await self.token_repo.set_is_revoked(reftoken, False)
            reftok= {"user_id":userid, "token": newreftoken, "expires_at": datetime.now() + timedelta(days=7)}
            refobj= await self.token_repo.insert_data(reftok, False)
            res= {"id": refobj.id, "userid": refobj.user_id}
            print(f"NEWREFRESH : {res}")
        return res

