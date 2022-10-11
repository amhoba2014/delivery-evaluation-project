import csv, pytz
from datetime import datetime
from typing import List

from . import models
from .database import SessionLocal
from sqlalchemy.orm import Session


class CSVRow:
    def __init__(self, source_longitude, source_latitude, destination_longitude, destination_latitude, weight,
                 time_window, eta, service_time, route_id, driver_id):
        self.source_longitude: float = float(source_longitude)
        self.source_latitude: float = float(source_latitude)
        self.destination_longitude: float = float(destination_longitude)
        self.destination_latitude: float = float(destination_latitude)
        self.weight: float = float(weight)
        self.time_window: int = int(time_window)
        self.eta: datetime = datetime.fromtimestamp(float(eta), tz=pytz.timezone('Iran'))
        self.service_time: float = float(service_time)
        self.route_id: int = int(route_id)
        self.driver_id: int = int(driver_id)


routes_list: List[models.Route] = []
deliveries_list: List[models.Deliverie] = []


def find_route_by_id(id: int):
    found_route: models.Route | None = None
    for route in routes_list:
        if route.id == id:
            found_route = route
    return found_route


def make_route(route_id, driver_id):
    route: models.Route
    found_route = find_route_by_id(route_id)
    if found_route is None:
        route = models.Route(
            id=route_id,
            driver_id=driver_id
        )
        routes_list.append(route)
    else:
        route = found_route

    return route


def import_csv():
    db: Session = SessionLocal()
    try:

        # This is an oversimplified check. We can make it more complex later
        check_if_db_filled = db.query(models.Deliverie).offset(0).limit(10).all()
        if len(check_if_db_filled) != 0:
            print("Notice: CSV file is already imported. No need to double import it.")
            return

        with open('./data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(reader):

                # Get rid of the header row
                if i == 0:
                    continue

                csv_row = CSVRow(*row)

                route = make_route(csv_row.route_id, csv_row.driver_id)
                deliverie = models.Deliverie(
                    source_latitude=csv_row.source_latitude,
                    source_longitude=csv_row.source_longitude,
                    destination_latitude=csv_row.destination_latitude,
                    destination_longitude=csv_row.destination_longitude,
                    weight=csv_row.weight,
                    time_window=csv_row.time_window,
                    eta=csv_row.eta,
                    service_time=csv_row.service_time,

                    route_id=route.id
                )
                deliveries_list.append(deliverie)

        db.add_all([*routes_list, *deliveries_list])
        db.commit()

        print("CSV file is imported successfully.")

    finally:
        db.close()
