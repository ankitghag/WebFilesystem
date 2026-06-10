from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_query import UserRepository
from app.repositories.fs_node_query import FSNodeRepository
from app.repositories.grp_query import GrpRepository
from app.repositories.token_query import TokenRepository
from app.services.fs_node_service import FSNodeService
from app.services.user_service import UserService
from app.services.storage_service import StorageService
from app.services.group_service import GroupService
from app.services.token_service import TokenService


from app.dependencies.dp_storage import get_storage_service


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db, UserRepository(db))

def get_node_service(db: AsyncSession = Depends(get_db), storage= Depends(get_storage_service)) -> FSNodeService:
    return FSNodeService(db, FSNodeRepository(db), storage)

def get_group_service(db: AsyncSession = Depends(get_db)):
    return GroupService(db, GrpRepository(db), UserRepository(db))

def get_token_service(db: AsyncSession = Depends(get_db)):
    return TokenService(db, TokenRepository(db))