import time

class BMP200:
    def __init__(self, i2c):
        self.i2c = i2c
        self.address = 0x77

    def read_pressure(self):
        # placeholder until driver is added
        return 1013.25

    def read_altitude(self):
        # simple fake altitude model for now
        return 0.0
