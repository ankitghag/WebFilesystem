from typing import List, Optional, Union

#from app.core.security import get_password_hash
from app.models.app_model import User
from app.repositories.user_query import UserRepository
from app.repositories.grp_query import GrpRepository
from app.schemas.sch_user import UserCreate, UserUpdate
from app.dtos.fs_node_dto import CreateGrpCmd
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.exceptions.http_exceptions import UserNotExsits, NotanAdmin

class GroupService:    
    def __init__(self, db: AsyncSession, grp_repo: GrpRepository, user_repo: UserRepository):
        """Initialize with user repository"""
        self.db = db
        self.user_repo = user_repo
        self.grp_repo= grp_repo

    async def create_grp(self, param: CreateGrpCmd):
        print(f'TYEP PARAN : {type(param)}| {param}')
        grparam= dict(param)
        async with self.db.begin():
            uobj= await self.user_repo.get_user(param.userid)
            print(uobj)
            if uobj is None:
                raise UserNotExsits("User does not exists", "USER_NOT_EXISTS")
            elif uobj[0].role != "ADMIN":
                raise NotanAdmin("User is not an Admin", "NOT_ADMIN")
            # grparam= {}
            # grparam["name"]= param.grpname
            # grparam["description"]=  param.grpdesc
            print(f"GRPARAm : {grparam}")
            lid= await self.grp_repo.insert_data(grparam, False)
            if lid is not None:
                grparam["grpid"]= lid
                res= await self.grp_repo.insert_user_grp(grparam, False)

        return res

