from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, importer
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
importer.import_csv()

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/get_the_number_of_deliveries/", response_model=schemas.GetTheNumberOfDeliveriesResponse)
def get_the_number_of_deliveries(input: schemas.GetTheNumberOfDeliveriesRequest, db: Session = Depends(get_db)):
    queue_deliveries: List[models.Deliverie] = db.query(models.Deliverie).filter(
        models.Deliverie.eta > input.date
    ).all()

    output_result_set: List[schemas.GetTheNumberOfDeliveriesResultSet] = []

    for deliverie in queue_deliveries:
        found = False
        for item in output_result_set:
            if item.time_window == deliverie.time_window:
                item.number_of_deliveries += 1
                found = True
                break
        if found is False:
            output_result_set.append(schemas.GetTheNumberOfDeliveriesResultSet(
                time_window=deliverie.time_window,
                number_of_deliveries=1
            ))

    return schemas.GetTheNumberOfDeliveriesResponse(result_set=output_result_set)


@app.post("/get_total_travel_and_service_time/", response_model=schemas.GetTotalTravelAndServiceTimeResponse)
def get_total_travel_and_service_time(input: schemas.GetTotalTravelAndServiceTimeRequest,
                                      db: Session = Depends(get_db)):
    all_routes = db.query(models.Route).all()
    all_drivers: List[int] = list(set([route.driver_id for route in all_routes]))

    each_driver_total_time: List[schemas.EachDriverTotalTime] = []

    for each_driver in all_drivers:

        related_routes: List[models.Route] = db.query(models.Route).filter(models.Route.driver_id == each_driver).all()
        related_deliveries: List[models.Deliverie] = []
        for route in related_routes:
            related_deliveries = related_deliveries + route.deliverie

        # Get all deliveries before the date
        all_deliveries_before_date: List[models.Deliverie] = []
        for rd in related_deliveries:
            if rd.eta < input.date:
                all_deliveries_before_date.append(rd)

        all_deliveries_before_date.sort(key=lambda x: x.eta)

        total_travel_time = all_deliveries_before_date[-1].eta.timestamp() - input.time_window
        total_service_time = sum([item.service_time for item in all_deliveries_before_date])

        each_driver_total_time.append(
            schemas.EachDriverTotalTime(
                driver_id=each_driver,
                total_travel_time=total_travel_time,
                total_service_time=total_service_time
            )
        )

    return schemas.GetTotalTravelAndServiceTimeResponse(each_driver_total_time=each_driver_total_time)
