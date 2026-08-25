from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, select

from app.database import get_session
from app.models.service_center import ServiceCenter
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.schemas.dashboard import DashboardSummary
from app.schemas.service_record import ServiceRecordRead
from app.schemas.vehicle import VehicleDueForService, VehicleRead

router = APIRouter()


@router.get("/{service_center_id}", response_model=DashboardSummary)
def get_dashboard(service_center_id: UUID, session: Session = Depends(get_session)):
    center = session.get(ServiceCenter, service_center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Service center not found")

    today = date.today()
    month_start = today.replace(day=1)

    center_vehicles = session.exec(
        select(Vehicle).where(Vehicle.home_service_center_id == service_center_id)
    ).all()

    records_this_month = session.exec(
        select(ServiceRecord).where(
            ServiceRecord.service_center_id == service_center_id,
            ServiceRecord.service_date >= month_start,
        )
    ).all()

    recent_records = session.exec(
        select(ServiceRecord)
        .where(ServiceRecord.service_center_id == service_center_id)
        .order_by(col(ServiceRecord.service_date).desc())
        .limit(10)
    ).all()

    due_vehicles: List[VehicleDueForService] = []
    for v in center_vehicles:
        km_overdue = v.current_odometer - (v.last_service_odometer + v.service_interval_km)
        days_since = (today - v.last_service_date).days if v.last_service_date else None
        time_overdue = days_since is not None and days_since >= v.service_interval_days

        if km_overdue >= 0 or time_overdue:
            vehicle_read = VehicleRead.model_validate(v)
            due_vehicles.append(
                VehicleDueForService(
                    **vehicle_read.model_dump(),
                    km_overdue=max(0.0, km_overdue),
                    days_since_last_service=days_since,
                )
            )

    return DashboardSummary(
        service_center_id=service_center_id,
        service_center_name=center.name,
        total_vehicles=len(center_vehicles),
        services_this_month=len(records_this_month),
        vehicles_due_count=len(due_vehicles),
        revenue_this_month=sum(r.cost for r in records_this_month if r.cost is not None),
        due_vehicles=due_vehicles,
        recent_service_records=[ServiceRecordRead.model_validate(r) for r in recent_records],
    )
