# pip install python-decouple
from decouple import config

DATABASE_URL = config(
    "DATABASE_URL",
    default="",
)
TIME_ZONE = config("TIME_ZONE", default="UTC")