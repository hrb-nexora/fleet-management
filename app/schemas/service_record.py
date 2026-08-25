from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceRecordCreate(BaseModel):
    vehicle_id: UUID
    service_center_id: UUID
    service_type: str
    odometer_at_service: float
    service_date: date
    notes: Optional[str] = None
    cost: Optional[float] = None


class ServiceRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_id: UUID
    service_center_id: UUID
    service_type: str
    odometer_at_service: float
    service_date: date
    notes: Optional[str]
    cost: Optional[float]
    created_at: datetime
