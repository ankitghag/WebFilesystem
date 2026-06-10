from sqlalchemy import Boolean, Column, DateTime,SmallInteger,Integer, String, func, Enum, TIMESTAMP, text, BigInteger, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "filesys"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    role: Mapped[str]=mapped_column(String(10))
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)  # suggest larger length
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("now()"))

    @property
    def role_enum(self) -> Optional[UserRole]:
        """Get role as enum object for type safety"""
        if self.role:
            try:
                return UserRole(self.role)
            except ValueError:
                return None
        return None

class FSNode(Base):
    __tablename__ = "fs_node"

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="fs_node_parent_name_key"),
        {"schema": "filesys"}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    is_directory: Mapped[bool] = mapped_column(Boolean,nullable=False)
    parent_id: Mapped[int | None] = mapped_column(BigInteger,
                ForeignKey(
                    "filesys.fs_node.id",
                    ondelete="CASCADE",
                    name="fs_node_parent_id_fkey"
                ),
    nullable=True
    )
    owner_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "filesys.users.id",
            name="fs_node_owner_id_fkey"
        ),
        nullable=False
    )
    path: Mapped[str | None] = mapped_column( String(1000))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=text("now()"),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=text("now()"),onupdate=text("now()"),nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean,server_default=text("false"),nullable=False)
    owner_perm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=7  # owner default 7
    )
    group_perm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0  # group default 0
    )
    other_perm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0  # other default 0
    )
    group_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("filesys.groups.id", name="fk_fs_node_group"),
        nullable=True
    )
    status: Mapped[int] = mapped_column(
        String(30),
        nullable=False,
        default="UPLOADING"  # Status default 0
    )

class UserGroup(Base):
    __tablename__ = "user_groups"
    __table_args__ = {"schema": "filesys"}

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("filesys.users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

    group_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("filesys.groups.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

class Group(Base):
    __tablename__ = "groups"
    __table_args__ = {"schema": "filesys"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "filesys"}

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("filesys.users.id", ondelete="CASCADE"),
        nullable=False
    )

    token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )