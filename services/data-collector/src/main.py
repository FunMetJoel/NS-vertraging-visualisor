import dotenv
import nsAPI
import sys
import database
from datetime import datetime
from time import sleep

dotenv.load_dotenv()
database.setup_database()

stations = nsAPI.get_stations()
if (stations is None):
    sys.exit("No stations found")

uicCodes = []
for station in stations:
    uicCodes.append(station.get("UICCode"))

    namen:dict = station.get("namen")
    if namen is None:
        namen = {}

    database.add_station_info(
        uicCode = station.get("UICCode"),
        lat = station.get("lat"),
        long = station.get("lng"),
        shortName=namen.get("kort"),
        middleName=namen.get("middel"),
        longName=namen.get("lang")
    )


def parse_datetime(value: str):
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")

while True:
    for uicCode in uicCodes:
        try:
            arrivals = nsAPI.get_arrivals(uicCode=uicCode)
            if arrivals is None:
                continue
            for arrival in arrivals["arrivals"]:
                database.add_arrival_info(
                    uicCode=uicCode,
                    time=parse_datetime(arrival.get("plannedDateTime")).date(),
                    productNumber=arrival.get("product").get("number"),
                    plannedArrival=parse_datetime(arrival.get("plannedDateTime")),
                    actualArrival=parse_datetime(arrival.get("actualDateTime")),
                    cancelled=arrival.get("cancelled"),
                    plannedTrack=arrival.get("plannedTrack"),
                    actualTrack=arrival.get("actualTrack")
                )
        except Exception as e:
            print(e)

        sleep(1)

    for uicCode in uicCodes:
            try:
                departures = nsAPI.get_departures(uicCode=uicCode)
                if departures is None:
                    continue
                for departure in departures["departures"]:
                    database.add_departure_info(
                        uicCode=uicCode,
                        time=parse_datetime(departure.get("plannedDateTime")).date(),
                        productNumber=departure.get("product").get("number"),
                        plannedDeparture=parse_datetime(departure.get("plannedDateTime")),
                        actualDeparture=parse_datetime(departure.get("actualDateTime")),
                        cancelled=departure.get("cancelled"),
                        plannedTrack=departure.get("plannedTrack"),
                        actualTrack=departure.get("actualTrack")
                    )
            except Exception as e:
                print(e)
    
            sleep(1)