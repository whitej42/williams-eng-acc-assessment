from fastapi import FastAPI, Depends
from .database import Base, engine
from .routers import health, drivers, circuits
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="F1 Stats API")

# Register routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(circuits.router, prefix="/circuits", tags=["Circuits"])

# Instrument the app for Prometheus
Instrumentator().instrument(app).expose(app)