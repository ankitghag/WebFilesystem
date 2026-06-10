from typing import Optional, Dict, Any,  Type
from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_model import Group, UserGroup
from app.repositories.base_query import BaseRepository

class GrpRepository(BaseRepository[Group]):
    """Repository for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Group)
    
    async def insert_user_grp(self, param: dict, commit_txn:Optional[bool]=True):
        stmt = insert(UserGroup).values(
            [{"user_id": uid, "group_id": param["grpid"]} for uid in param["grpuserids"]]
        )
        res= await self.db.execute(stmt)
        if commit_txn:
            await self.db.commit()
        return res


    async def insert_data(self, param: Dict[str,Any], commit_txn:Optional[bool]=True):
        processed_data = {}
        query = (insert(Group).values(name= param["grpname"], description= param["grpdesc"]).returning(Group.id))
        result = await self.db.execute(query)
        if commit_txn:
            await self.db.commit()
        return result.scalar_one_or_none()

        