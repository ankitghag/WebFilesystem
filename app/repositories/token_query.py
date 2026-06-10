from typing import Optional, Dict, Any
from sqlalchemy import select, func, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_model import RefreshToken
from app.repositories.base_query import BaseRepository

class TokenRepository(BaseRepository[RefreshToken]):
    """Repository for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with database session.
        
        Args:
            db: SQLAlchemy async session
        """
        super().__init__(db, RefreshToken)

    # await db.execute(
    #     "UPDATE refresh_tokens SET is_revoked=TRUE WHERE token=:token",
    #     {"token": refresh_token}
    # )
    async def get_ref_token(self, reftok, commit_txn=True):
        query= select(RefreshToken).where(RefreshToken.token == reftok)
        result= await self.db.execute(query)
        if commit_txn:
            await self.db.commit()
        return result.one_or_none()
    async def set_is_revoked(self, reftok, commit_txn= True):
        query= update(RefreshToken).where(RefreshToken.token == reftok).values(is_revoked=True)
        print(query) # This prints the SQL string
        result= await self.db.execute(query)
        if commit_txn:
            await self.db.commit()
        return result

    # async def (self, reftok, commit_txn= True):
     # await db.execute(
    #     "INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (:uid, :token, :exp)",
    #     {"uid": payload["user_id"], "token": new_refresh_token, "exp": datetime.utcnow() + timedelta(days=7)}
    # )
