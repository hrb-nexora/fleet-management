from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.service_record import ServiceRecordRead
from app.schemas.vehicle import VehicleDueForService


class DashboardSummary(BaseModel):
    service_center_id: UUID
    service_center_name: str
    total_vehicles: int
    services_this_month: int
    vehicles_due_count: int
    revenue_this_month: float
    due_vehicles: List[VehicleDueForService]
    recent_service_records: List[ServiceRecordRead]
