from fastapi import FastAPI
from api.routers import drivers, circuits
from api.database import Base, engine

app = FastAPI(title="F1 Stats API")

# Register routers
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(circuits.router, prefix="/circuits", tags=["Circuits"])

# Create tables on startup
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
