from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.schemas.service_record import ServiceRecordCreate, ServiceRecordRead

router = APIRouter()


@router.post("/", response_model=ServiceRecordRead, status_code=201)
def create_service_record(payload: ServiceRecordCreate, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, payload.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    record = ServiceRecord(**payload.model_dump())
    session.add(record)

    # keep vehicle odometer and last-service info in sync
    if payload.odometer_at_service > vehicle.current_odometer:
        vehicle.current_odometer = payload.odometer_at_service
    vehicle.last_service_odometer = payload.odometer_at_service
    vehicle.last_service_date = payload.service_date
    session.add(vehicle)

    session.commit()
    session.refresh(record)
    return record


@router.get("/{record_id}", response_model=ServiceRecordRead)
def get_service_record(record_id: UUID, session: Session = Depends(get_session)):
    record = session.get(ServiceRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Service record not found")
    return record
