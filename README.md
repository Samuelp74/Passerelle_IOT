# Mini-projet for 4IRC students at CPE Lyon

## Installing the server

### In any environment (Windows, linux, mac) for the database and grafana:

```
docker compose up -d
```

### For the passerel

> Create a python venv with dependencies in requirements.txt file
> modify the serial port in uart/uart.py

    - COMX for Windows
    - /dev/tty.usbmodemXXXXX for mac
    - /dev/ttyX for Linux)

> copy .env.example to .env and put your values there or do not change it

## Sources

- [timescaledb-python](https://github.com/jmitchel3/timescaledb-python)
- [sqlmodel-doc](https://sqlmodel.tiangolo.com/tutorial)
- [timescale](https://docs.timescale.com)
