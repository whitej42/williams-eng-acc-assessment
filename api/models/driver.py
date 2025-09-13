from sqlalchemy import Column, Integer, String
from api.database import Base

class Driver(Base):
    __tablename__ = "drivers_summary"

    driverId = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    races_entered = Column(Integer, default=0)
    podiums = Column(Integer, default=0)
    wins = Column(Integer, default=0)
