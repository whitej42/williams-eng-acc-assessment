'''
Cricuit Model

Defines the ORM model for circuits, summarising
statistics such as total races, fastest laps and fastest driver.
'''

from sqlalchemy import Column, Integer, String

from ..database import Base


class Circuit(Base):
    __tablename__ = "circuits_summary"

    circuitId = Column(Integer, primary_key=True)
    circuit_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    country = Column(String, nullable=True)
    total_races = Column(Integer, default=0)
    fastest_lap = Column(Integer, default=0)
    fastest_driver = Column(Integer, nullable=True)
