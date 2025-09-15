from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.driver import DriverOutput
from ..database import get_db
from ..models.driver import Driver

router = APIRouter()


@router.get("/", response_model=list[DriverOutput])
def get_drivers(
        db: Session = Depends(get_db)
    ):
    
    return db.query(Driver).all()

@router.get("/{driver_id}", response_model=DriverOutput)
def get_driver(
        driver_id: str, 
        db: Session = Depends(get_db)
    ):

    driver = db.query(Driver).filter(Driver.driverId == driver_id).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver