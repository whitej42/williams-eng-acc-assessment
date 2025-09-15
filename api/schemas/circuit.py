from pydantic import BaseModel

class CircuitOutput(BaseModel):
    circuitId: int
    circuit_name: str
    location: str
    country: str
    total_races: int
    fastest_lap: int
    fastest_driver: int

    class Config:
        from_attributes = True