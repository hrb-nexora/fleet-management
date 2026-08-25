from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, col, select

from app.database import get_session
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.schemas.service_record import ServiceRecordRead
from app.schemas.vehicle import VehicleCreate, VehicleDueForService, VehicleRead

router = APIRouter()


@router.post("/", response_model=VehicleRead, status_code=201)
def create_vehicle(payload: VehicleCreate, session: Session = Depends(get_session)):
    vehicle = Vehicle(**payload.model_dump())
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.get("/", response_model=List[VehicleRead])
def list_vehicles(
    service_center_id: Optional[UUID] = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(Vehicle)
    if service_center_id:
        stmt = stmt.where(Vehicle.home_service_center_id == service_center_id)
    return session.exec(stmt).all()


# static route must be declared before /{vehicle_id} to avoid shadowing
@router.get("/due-for-service", response_model=List[VehicleDueForService])
def get_vehicles_due_for_service(
    service_center_id: Optional[UUID] = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(Vehicle)
    if service_center_id:
        stmt = stmt.where(Vehicle.home_service_center_id == service_center_id)
    vehicles = session.exec(stmt).all()

    today = date.today()
    due = []
    for v in vehicles:
        km_overdue = v.current_odometer - (v.last_service_odometer + v.service_interval_km)
        days_since = (today - v.last_service_date).days if v.last_service_date else None
        time_overdue = days_since is not None and days_since >= v.service_interval_days

        if km_overdue >= 0 or time_overdue:
            vehicle_read = VehicleRead.model_validate(v)
            due.append(
                VehicleDueForService(
                    **vehicle_read.model_dump(),
                    km_overdue=max(0.0, km_overdue),
                    days_since_last_service=days_since,
                )
            )
    return due


@router.get("/{vehicle_id}/service-history", response_model=List[ServiceRecordRead])
def get_vehicle_service_history(vehicle_id: UUID, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    records = session.exec(
        select(ServiceRecord)
        .where(ServiceRecord.vehicle_id == vehicle_id)
        .order_by(col(ServiceRecord.service_date).desc())
    ).all()
    return records


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(vehicle_id: UUID, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.patch("/{vehicle_id}/odometer", response_model=VehicleRead)
def update_odometer(vehicle_id: UUID, odometer: float, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if odometer < vehicle.current_odometer:
        raise HTTPException(status_code=400, detail="Odometer cannot decrease")
    vehicle.current_odometer = odometer
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle
