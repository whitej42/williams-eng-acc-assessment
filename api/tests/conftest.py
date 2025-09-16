import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import Base, get_db
from ..models.driver import Driver
from ..models.circuit import Circuit

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

'''
Override get_db to use the test database
'''
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override get_db to use the test database
app.dependency_overrides[get_db] = override_get_db

'''
Setup test database and seed test data
'''
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Bootstrap database
    Base.metadata.create_all(bind=engine)

    # Seed test data
    db = TestingSessionLocal()

    try:
        db.query(Driver).delete()
        db.query(Circuit).delete()
        db.commit()

        driver = Driver(
            driverId=1,
            name="Lewis Hamilton",
            races_entered=100,
            podiums=50,
            wins=30
        )
        db.add(driver)
        db.commit()
        
        circuit = Circuit(
            circuitId=1,
            circuit_name="Silverstone",
            location="Silverstone",
            country="United Kingdom",
            total_races=200,
            fastest_lap=100,
            fastest_driver=1
        )
        db.add(circuit)
        db.commit()
    finally:
        db.close()