-- Drivers Summary Table
-- Polled from drivers and driver_standings tables

CREATE OR REPLACE TABLE drivers_summary AS
SELECT 
    d.driverId,
    d.forename || ' ' || d.surname AS name,
    COUNT(r.driverId) AS races_entered,
    SUM(
        CASE
            WHEN r.position <= 3 THEN 1 
            ELSE 0 END
        ) AS podiums,
    SUM(r.position = 1) AS wins
FROM drivers d
JOIN driver_standings r ON d.driverId = r.driverId
GROUP BY d.driverId, name
ORDER BY d.driverId;


-- Circuits Summary Table
-- Polled from circuits, races and lap_times tables

CREATE OR REPLACE TEMPORARY TABLE fastest_laps AS
-- Temp table for fastest laps
-- Prevents many-to-many relationship
SELECT
    ra.circuitId,
    MIN(l.milliseconds) AS fastest_lap,
    ARG_MIN(l.driverId, l.milliseconds) AS fastest_driver
FROM lap_times l
JOIN races ra ON ra.raceId = l.raceId
GROUP BY ra.circuitId;

CREATE OR REPLACE TABLE circuits_summary AS
SELECT
    c.circuitId,
    c.name AS circuit_name,
    c.location,
    c.country,
    COUNT(DISTINCT ra.raceId) AS total_races,
    f.fastest_lap,
    f.fastest_driver
FROM circuits c
JOIN races ra ON ra.circuitId = c.circuitId
JOIN fastest_laps f ON c.circuitId = f.circuitId
GROUP BY c.circuitId, circuit_name, c.location, c.country, f.fastest_lap, f.fastest_driver
ORDER BY c.circuitId;