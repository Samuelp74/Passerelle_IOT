from random import random

from timescale.crud import create

N = 100

# fake data factory
def factory():
    types = {"temperature", "humidity", "luminosity"}
    # temperature
    for _ in range(N):
        r = (random() * 20) + 15
        value = str(r)
        create(value=value, label="temperature")
    # humidity
    for _ in range(N):
        r = (random() * 10) + 35
        value = str(r)
        create(value=value, label="humidity")
    # luminosity
    for _ in range(N):
        r = random() * 100
        value = str(r)
        create(value=value, label="luminosity")