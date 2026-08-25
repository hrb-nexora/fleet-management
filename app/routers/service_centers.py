from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from app.database import get_session
from app.models.service_center import ServiceCenter

router = APIRouter()


class ServiceCenterCreate(BaseModel):
    name: str
    location: Optional[str] = None


class ServiceCenterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    location: Optional[str]


@router.post("/", response_model=ServiceCenterRead, status_code=201)
def create_service_center(payload: ServiceCenterCreate, session: Session = Depends(get_session)):
    center = ServiceCenter(**payload.model_dump())
    session.add(center)
    session.commit()
    session.refresh(center)
    return center


@router.get("/", response_model=List[ServiceCenterRead])
def list_service_centers(session: Session = Depends(get_session)):
    return session.exec(select(ServiceCenter)).all()


@router.get("/{center_id}", response_model=ServiceCenterRead)
def get_service_center(center_id: UUID, session: Session = Depends(get_session)):
    center = session.get(ServiceCenter, center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Service center not found")
    return center
