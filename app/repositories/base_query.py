from typing import Dict, Generic, List, Optional, Type, TypeVar, Any, Tuple
from sqlalchemy import func, select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Any)

class BaseRepository(Generic[ModelType]):
    """
    Base repository with common database operations.
    
    Generic repository that provides basic CRUD operations for SQLAlchemy models.
    """
    
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        """
        Initialize the repository with database session and model class.
        
        Args:
            db: SQLAlchemy async session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    
    async def insert_data(self, user: Dict[str,Any], commit_txn:Optional[bool]=True)->ModelType:
        processed_data = {}
        for key, value in user.items():
            if hasattr(value, 'value'):  # enum objects have .value attribute
                processed_data[key] = value.value
            else:
                processed_data[key] = value
                
        print(processed_data)
        db_obj = self.model(**processed_data)
        self.db.add(db_obj)
        if commit_txn and commit_txn == True:
            await self.db.commit()
            await self.db.refresh(db_obj)
        return db_obj
