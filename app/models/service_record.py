from datetime import date
from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.base import UUIDBase


class ServiceRecord(UUIDBase, table=True):
    __tablename__ = "service_records"

    vehicle_id: UUID = Field(foreign_key="vehicles.id")
    service_center_id: UUID = Field(foreign_key="service_centers.id")
    service_type: str
    odometer_at_service: float
    service_date: date
    notes: Optional[str] = Field(default=None)
    cost: Optional[float] = Field(default=None)
