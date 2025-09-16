'''
Drivers Router

Defines API endpoints for interacting with the Drivers model
'''

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.driver import DriverOutput
from ..database import get_db
from ..models.driver import Driver

router = APIRouter()

'''
GET /drivers/

Returns all drivers
'''
@router.get("/", response_model=list[DriverOutput])
def get_drivers(
        db: Session = Depends(get_db)
    ):
    
    try:
        return db.query(Driver).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
GET /drivers/{driver_id}

Returns a driver by their ID
'''
@router.get("/{driver_id}", response_model=DriverOutput)
def get_driver(
        driver_id: int, 
        db: Session = Depends(get_db)
    ):

    try:
        driver = db.query(Driver).filter(Driver.driverId == driver_id).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))