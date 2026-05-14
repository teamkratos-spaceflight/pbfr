from enum import Enum

class FlightState(Enum):
    BOOT = 0
    READY = 1
    ARMED = 2
    ASCENT = 3
    APOGEE = 4
    DESCENT = 5
    LANDED = 6
    FAULT = 7
    DOWNLOAD = 8