'''
Driver Base Model

Defines base schema for the driver model
'''

from pydantic import BaseModel

class DriverOutput(BaseModel):
    driverId: int
    name: str
    races_entered: int
    podiums: int
    wins: int

    class Config:
        from_attributes = True