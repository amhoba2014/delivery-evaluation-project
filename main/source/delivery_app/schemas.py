from typing import List

from pydantic import BaseModel, validator
from datetime import datetime
import pytz


class GetTheNumberOfDeliveriesRequest(BaseModel):
    date: datetime

    @validator("date")
    def date_validate(cls, date: datetime):
        return datetime.fromtimestamp(date.timestamp(), tz=pytz.timezone('Iran'))


class GetTheNumberOfDeliveriesResultSet(BaseModel):
    time_window: int
    number_of_deliveries: int


class GetTheNumberOfDeliveriesResponse(BaseModel):
    result_set: List[GetTheNumberOfDeliveriesResultSet]


####################################################################################################


class GetTotalTravelAndServiceTimeRequest(BaseModel):
    date: datetime
    time_window: int

    @validator("date")
    def date_validate(cls, date: datetime):
        return datetime.fromtimestamp(date.timestamp(), tz=pytz.timezone('Iran'))


class EachDriverTotalTime(BaseModel):
    driver_id: int
    total_travel_time: int
    total_service_time: int


class GetTotalTravelAndServiceTimeResponse(BaseModel):
    each_driver_total_time: List[EachDriverTotalTime]
