from datetime import date
from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDBase


class Vehicle(UUIDBase, table=True):
    __tablename__ = "vehicles"

    license_plate: str = Field(unique=True, index=True)
    make: str
    model: str
    year: int
    home_service_center_id: UUID = Field(foreign_key="service_centers.id")
    current_odometer: float = Field(default=0.0)
    service_interval_km: float = Field(default=10000.0)
    service_interval_days: int = Field(default=180)
    last_service_odometer: float = Field(default=0.0)
    last_service_date: Optional[date] = Field(default=None)
