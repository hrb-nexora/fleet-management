from sqlmodel import Field

from app.models.base import UUIDBase


class ServiceCenter(UUIDBase, table=True):
    __tablename__ = "service_centers"

    name: str = Field(index=True)
