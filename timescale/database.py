from sqlmodel import Session, SQLModel, select

import timescaledb
from .models import SensorType


from .config import (
    DATABASE_URL,
    TIME_ZONE,
)

# time zone focused wrapper for sqlmodel.create_engine/sqlalchemy.create_engine
engine = timescaledb.create_engine(DATABASE_URL, timezone=TIME_ZONE, echo=True)


def init_db():
    # Create hypertables
    SQLModel.metadata.create_all(engine)
    timescaledb.metadata.create_all(engine)

    # auto insert default
    tmp = SensorType(label="temperature", unit="°C")
    lum = SensorType(label="luminosity", unit="lux")
    hum = SensorType(label="humidity", unit="%")

    with Session(engine) as session:
        query = select(SensorType).where(SensorType.label == "temperature")
        if session.exec(query) is None:
            session.add(tmp)
            session.add(lum)
            session.add(hum)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session