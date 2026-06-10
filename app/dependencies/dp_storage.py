from app.core.storage import get_r2_client
from app.services.storage_service import StorageService
from fastapi import Depends

def get_storage_service(r2client = Depends(get_r2_client)) -> StorageService:
    return StorageService(r2client, "webfsbucket")