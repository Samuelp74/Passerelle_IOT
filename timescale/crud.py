from datetime import datetime, timedelta, timezone

from timescale.models import Sensor, SensorRead, SensorCreate, SensorType, SensorTypeRead
from timescale.database import get_session
from sqlmodel import desc, Session, select

def create(value: str, label: str):
    # init 
    val = float(value)
    # yield session from engine
    session = next(get_session())
    # get sensor type from label sent
    query_type = select(SensorType).where(SensorType.label == label)
    sensor_type = session.exec(query_type).first()
    if sensor_type is None:
        return
    
    # db transaction
    sensor_create = SensorCreate(value=val, type_sensor=sensor_type.id)
    # validate fields
    # missing sensor_type.id ?
    # value not valid ?
    sensor = Sensor.model_validate(sensor_create)
    session.add(sensor)
    session.commit()

# read only first entry 
def read(t: str | None):
    session = next(get_session())
    query_sensor = select(Sensor, SensorType).join(SensorType)
    if t is not None:
        query_sensor = query_sensor.where(SensorType.label == t)
    sensor, sensortype = session.exec(query_sensor).first()
    if sensor is None or sensortype is None:
        return None

    sensor_read = sensor.to_read_entity(sensortype)
    return sensor_read

# all entry of sensors
def read_all():
    session = next(get_session())
    query_sensor = select(Sensor, SensorType).order_by(desc(Sensor.time))
    sensors = session.exec(query_sensor)

    sensors_read = map(lambda x, y:  x.to_read_entity(y), sensors)
    return sensors_read

def read_sensor_type(type: str):
    session = next(get_session())
    query = select(SensorType).where(SensorType.label == type)
    return session.exec(query)