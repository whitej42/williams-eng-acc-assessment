from pydantic import BaseModel

class DriverOutput(BaseModel):
    driverId: int
    name: str
    races_entered: int
    podiums: int
    wins: int

    class Config:
        from_attributes = True