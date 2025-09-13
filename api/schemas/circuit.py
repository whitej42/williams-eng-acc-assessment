from pydantic import BaseModel

class CircuitOutput(BaseModel):
    circuit_name: str
    location: str
    country: str
    total_races: int
    fastest_lap: int

    class Config:
        from_attributes = True