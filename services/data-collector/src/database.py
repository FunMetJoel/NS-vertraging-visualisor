import os
import sqlite3
import datetime as dt

db_path = None

def setup_database():
    global db_path
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    os.makedirs(data_dir, exist_ok=True)

    db_path = os.path.join(data_dir, "database.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS station (
            uicCode STRING PRIMARY KEY,
            lat FLOAT,
            long FLOAT,
            shortName STRING,
            middleName STRING,
            longName STRING
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trainStop (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uicCode STRING NOT NULL,
            time DATETIME NOT NULL,
            productNumber STRING NOT NULL,
            plannedArrival DATETIME,
            actualArrival DATETIME,
            plannedDeparture DATETIME,
            actualDeparture DATETIME,
            cancelled BOOLEAN,
            plannedTrack VARCHAR(5),
            actualTrack VARCHAR(5),
            CONSTRAINT unique_uicCode_time_productNumber UNIQUE (uicCode, time, productNumber),
            FOREIGN KEY(uicCode) REFERENCES station(uicCode)
        )
        """
    )

    connection.commit()
    connection.close()

    return db_path

def add_arrival_info(uicCode, time:dt.datetime, productNumber:str, plannedArrival:dt.datetime, actualArrival:dt.datetime, cancelled:bool, plannedTrack:str, actualTrack:str):
    if db_path is None:
        return

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO trainStop (uicCode, time, productNumber, plannedArrival, actualArrival, cancelled, plannedTrack, actualTrack)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(uicCode, time, productNumber)
        DO UPDATE SET
            plannedArrival = excluded.plannedArrival,
            actualArrival = excluded.actualArrival,
            cancelled = excluded.cancelled,
            plannedTrack = excluded.plannedTrack,
            actualTrack = excluded.actualTrack
        """,
        (uicCode, time, productNumber, plannedArrival, actualArrival, cancelled, plannedTrack, actualTrack),
    )

    connection.commit()
    connection.close()

def add_departure_info(uicCode, time:dt.datetime, productNumber:str, plannedDeparture:dt.datetime, actualDeparture:dt.datetime, cancelled:bool, plannedTrack:str, actualTrack:str):
    if db_path is None:
        return

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO trainStop (uicCode, time, productNumber, plannedDeparture, actualDeparture, cancelled, plannedTrack, actualTrack)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(uicCode, time, productNumber)
        DO UPDATE SET
            plannedDeparture = excluded.plannedDeparture,
            actualDeparture = excluded.actualDeparture,
            cancelled = excluded.cancelled,
            plannedTrack = excluded.plannedTrack,
            actualTrack = excluded.actualTrack
        """,
        (uicCode, time, productNumber, plannedDeparture, actualDeparture, cancelled, plannedTrack, actualTrack),
    )

    connection.commit()
    connection.close()

def add_station_info(uicCode:str, lat:float, long:float, shortName:str, middleName:str, longName:str):
    if db_path is None:
        return

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO station (uicCode, lat, long, shortName, middleName, longName)
            VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(uicCode)
        DO UPDATE SET
            lat = excluded.lat,
            long = excluded.long,
            shortName = excluded.shortName,
            middleName = excluded.middleName,
            longName = excluded.longName
        """,
        (uicCode, lat, long, shortName, middleName, longName),
    )

    connection.commit()
    connection.close()
