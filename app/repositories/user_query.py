from typing import Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_model import User, UserGroup, Group
from app.repositories.base_query import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with database session.
        
        Args:
            db: SQLAlchemy async session
        """
        super().__init__(db, User)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: User email address
            
        Returns:
            User if found, None otherwise
        """
        # Perform a query to find the user by email
        # make case insensitive        
        query = select(User).where(func.lower(User.email) == email.lower())
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user(self, uid):
        qry= select(User).where(User.id == uid)        
        result= await self.db.execute(qry)
        robj= result.one_or_none()
        return robj

    async def get_user_grp_id(self, uid):
        qry= select(UserGroup).where(UserGroup.user_id == uid)
        result= await self.db.execute(qry)
        robj= result.one_or_none()
        return robj.group_id if robj else None
    