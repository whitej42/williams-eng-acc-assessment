'''
Circuits Router

Defines API endpoints for interacting with the Circuits model.
'''

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.circuit import CircuitOutput
from ..database import get_db
from ..models.circuit import Circuit

router = APIRouter()

'''
GET /circuits/

Returns all circuits
'''
@router.get("/", response_model=list[CircuitOutput])
def list_circuits(
        db: Session = Depends(get_db)
    ):

    return db.query(Circuit).all()

'''
GET /circuits/{circuit_id}

Returns circuit by their ID
'''
@router.get("/{circuit_id}", response_model=CircuitOutput)
def get_circuit(
        circuit_id: int, 
        db: Session = Depends(get_db)
    ):

    circuit = db.query(Circuit).filter(Circuit.circuitId == circuit_id).first()
    
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit