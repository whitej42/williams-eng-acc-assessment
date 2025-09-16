'''
Driver Model

Defines the ORM model for drivers, summarising their
statistics such as races entered, podiums, and wins.
'''

from sqlalchemy import Column, Integer, String
from ..database import Base


class Driver(Base):
    __tablename__ = "drivers_summary"

    driverId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    races_entered = Column(Integer, default=0)
    podiums = Column(Integer, default=0)
    wins = Column(Integer, default=0)
