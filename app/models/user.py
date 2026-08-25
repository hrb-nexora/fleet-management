from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDBase


class User(UUIDBase, table=True):
    __tablename__ = "users"

    name: str
    email: str = Field(unique=True, index=True)
    role: str = Field(default="manager")
    service_center_id: Optional[UUID] = Field(default=None, foreign_key="service_centers.id")