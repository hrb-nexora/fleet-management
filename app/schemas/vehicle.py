from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    license_plate: str
    make: str
    model: str
    year: int
    home_service_center_id: UUID
    current_odometer: float = 0.0
    service_interval_km: float = 10000.0
    service_interval_days: int = 180


class VehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    license_plate: str
    make: str
    model: str
    year: int
    home_service_center_id: UUID
    current_odometer: float
    service_interval_km: float
    service_interval_days: int
    last_service_odometer: float
    last_service_date: Optional[date]


class VehicleDueForService(VehicleRead):
    km_overdue: float
    days_since_last_service: Optional[int]
