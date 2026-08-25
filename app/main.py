from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import dashboard, service_centers, service_records, vehicles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Fleet Management API", version="1.0.0", lifespan=lifespan)

app.include_router(service_centers.router, prefix="/service-centers", tags=["Service Centers"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(service_records.router, prefix="/service-records", tags=["Service Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
