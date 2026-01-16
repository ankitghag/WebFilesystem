from typing import Optional, Dict, Any
from sqlalchemy import select, func, delete, exists, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_model import FSNode, UserGroup
from app.repositories.base_query import BaseRepository
from app.exceptions.http_exceptions import NotaDirectory, NotaOwner

class FSNodeRepository(BaseRepository[FSNode]):
    """Repository for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with database session.
        
        Args:
            db: SQLAlchemy async session
        """
        super().__init__(db, FSNode)
    
    async def get_user_grp_id(self, uid):
        qry= select(UserGroup).where(UserGroup.user_id == uid)
        result= await self.db.execute(qry)
        robj= result.scalar_one_or_none()
        return robj.group_id if robj else None

    async def chk_parent(self, param):
        chk_parent= select(FSNode).where(FSNode.id == param["parent_id"])
        result = await self.db.execute(chk_parent)
        return result.scalar_one_or_none()
        
    async def add_node(self, param):
        print(f"PARAM :PAR {param['parent_id']}")
        chk_parent= select(FSNode).where(FSNode.id == param["parent_id"])
        result = await self.db.execute(chk_parent)
        parent = result.scalar_one_or_none()
        print(f"CHKPARENT {parent}")
        if parent is None or not parent.is_directory:
            raise NotaDirectory("Parent is not a directory", "NOT_DIRECTORY")
        return await self.insert_data(param)

    async def dir_has_child(self, param):
        # considering parent id will always directory as insert operation has check 
        chk_child= select(exists().where(FSNode.parent_id == param["id"])) 
        result = await self.db.execute(chk_child)
        return True if result.scalar_one() > 0 else False

    async def delete_node(self, param, commit_txn: Optional[bool]=  True):
        query = delete(FSNode).where(FSNode.id == param["id"], FSNode.owner_id == param["owner_id"])
        result = await self.db.execute(query)
        if commit_txn:
            await self.db.commit()
        print(f"DEL RES : {result}")
        return result
    
    async def delete_empty_node(self, param, commit_txn: Optional[bool]= True):
        child_exists = select(FSNode).where(FSNode.parent_id == param["id"]).exists()
        query= delete(FSNode).where(FSNode.id == param["id"]).where(~child_exists)
        print(query) # This prints the SQL string
        result= await self.db.execute(query)
        if commit_txn:
            await self.db.commit()
        return result

    async def move_node(self, param, commit_txn: Optional[bool]= True):
        stmt = (update(FSNode).where(FSNode.id == param["id"]).values(parent_id=param["parent_id"]))
        result= await self.db.execute(stmt)
        if commit_txn:
            await self.db.commit()
        return result

    async def chk_owner(self, param):
        chk_own= select(FSNode).where(FSNode.id == param["nid"], FSNode.owner_id == param["owner_id"])
        result= await  self.db.execute(chk_own)
        return result.scalar_one_or_none()

    async def chg_node_perm(self, param):
        # print(f"ISOWN : {isown.owner_id}")
        ownp, grpp, othp= param["perm"]
        qry=  (update(FSNode). where(FSNode.id == param["nid"]).values(owner_perm=ownp, group_perm=grpp, other_perm=othp))
        result= await self.db.execute(qry)
        await self.db.commit()
        return result


        