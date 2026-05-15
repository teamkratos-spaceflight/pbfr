import time
from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from flight.statetones import STATETONES
class IMU:
    def __init__(self, i2c):
        self.i2c = i2c

    def read_acceleration(self):
        # fake for now (standing)
        ax = 0.0
        ay = 0.0
        az = 9.81
        return ax, ay, az

    def boot_test(self):
        buzzer = Buzzer(15)
        led = StatusLED()

        buzzer.beep(0.1, 1200)
        print("## IMU MPU6080 BOOT TEST ##")

        if self.read_acceleration()[0] < 1:
            print("!!! MPU6080 ACCELERATION TEST FAILED !!!")
            print(f"EXPECTED 100+ ACCEL GOT {self.read_acceleration()[0]}")
            while True:
                led.toggle()
                buzzer.beep(0.1, 400)
                time.sleep(0.5)
                led.toggle()
                buzzer.beep(0.1, 1200)



