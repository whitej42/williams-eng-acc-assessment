from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.circuit import CircuitOutput
from ..database import get_db
from ..models.circuits import Circuit

router = APIRouter()

circuits: list[CircuitOutput] = []

@router.get("/", response_model=list[CircuitOutput])
def list_circuits(db: Session = Depends(get_db)):
    return db.query(Circuit).all()

@router.get("/{circuit_id}", response_model=CircuitOutput)
def get_circuit(circuit_id: int, db: Session = Depends(get_db)):
    circuit = db.query(Circuit).filter(Circuit.circuitId == circuit_id).first()
    
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit