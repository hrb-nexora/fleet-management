from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDBase


class Vehicle(UUIDBase, table=True):
    __tablename__ = "vehicles"

    home_service_center_id: UUID = Field(foreign_key="service_centers.id")
    current_odometer: float = Field(default=0.0)
