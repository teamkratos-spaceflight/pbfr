class IMU:
    def __init__(self, i2c):
        self.i2c = i2c

    def read_acceleration(self):
        return 9.81