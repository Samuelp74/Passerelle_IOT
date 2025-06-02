from datetime import datetime
from sqlmodel import Field, SQLModel
from timescaledb import TimescaleModel

############
## Sensor type CQRS Hypertable
############
class SensorType(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    label: str = Field(index=True)
    unit: str

## Command
############
class SensorTypeCreate(SQLModel):
    label: str

## Query
############
class SensorTypeRead(SQLModel):
    id: int
    label: str
    unit: str

############
## température CQRS Hypertable
############
class Sensor(TimescaleModel, table=True):
    type_sensor: int = Field(foreign_key="sensortype.id", index=True)
    value: float

    __enable_compression__ = True
    __chunk_time_interval__ = "INTERVAL 1 days"
    __compress_orderby__ = "time"
    __compress_segmentby__ = "value"
    __drop_after__ = "INTERVAL 14 day"

    def to_read_entity(self, type: SensorType):
        return SensorRead(id=self.id, value=self.value, type_sensor=type.label, unit=type.unit, time=self.time)

## Command
############
class SensorCreate(SQLModel):
    value: float
    type_sensor: int

## Query
############
class SensorRead(SQLModel):
    id: int
    value: float
    type_sensor: str
    unit: str
    time: datetime = Field(default=None)

    def to_dict(self):
        return {column: getattr(self, column) for column in self.__fields__}