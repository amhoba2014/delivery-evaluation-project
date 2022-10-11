from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Deliverie(Base):
    __tablename__ = "Deliverie"

    id = Column(Integer, primary_key=True, index=True)
    source_latitude = Column(Float)
    source_longitude = Column(Float)
    destination_latitude = Column(Float)
    destination_longitude = Column(Float)
    weight = Column(Float)
    time_window = Column(Integer)
    eta = Column(DateTime(timezone=True))
    service_time = Column(Float)

    route_id = Column(Integer, ForeignKey("Route.id"))


class Route(Base):
    __tablename__ = "Route"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer)

    deliverie = relationship("Deliverie")
