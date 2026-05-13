class IMU:
    def __init__(self, i2c):
        self.i2c = i2c

    def read_acceleration(self):
        # fake for now (standing)
        ax = 0.0
        ay = 0.0
        az = 9.81
        return ax, ay, az
