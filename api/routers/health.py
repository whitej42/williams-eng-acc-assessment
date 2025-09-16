'''
Health Router

Defines API endpoints for interacting with health checks.
'''

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

'''
GET /health/

Performs a health check on the API.
Useful for Docker to esnure API service is running.

Returns a JSON response with the health status
'''
@router.get("/")
def get_health():
    return {"status": "OK"}

'''
GET /health/db

Performs a health check on the database.
Useful for Docker to ensure database service is running.

Returns a JSON response with the health status
'''
@router.get("/db")
def get_db_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))