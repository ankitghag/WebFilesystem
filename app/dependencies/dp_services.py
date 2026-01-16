from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_query import UserRepository
from app.repositories.fs_node_query import FSNodeRepository
from app.services.fs_node_service import FSNodeService
from app.services.user_service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db, UserRepository(db))

def get_node_service(db: AsyncSession = Depends(get_db)) -> FSNodeService:
    return FSNodeService(db, FSNodeRepository(db))