import time

from hardware.led import StatusLED
from hardware.buzzer import Buzzer

buzzer = Buzzer(15)
led = StatusLED()

class SDLogger:
    def __init__(self):
        self.file = None

    def start(self):
        self.file = open("flight.csv", "w")
        self.file.write("t,ax,ay,az\n")

    def log(self, t, ax, ay, az):
        if self.file:
            self.file.write(f"{t},{ax},{ay},{az}\n")

    def close(self):
        if self.file:
            self.file.close()

    def boot_test(self):
        print("## SDCard Boot Test ##")

        with open("test.dat", "w") as file:
            file.write("1")

        with open("test.dat", "r") as file:
            result = file.read()

        if result == "1":
            print("SDCard Boot Test: PASSED")
        else:
            print("SDCard Boot Test: FAILED")

            while True:
                led.on()
                buzzer.beep(0.2, 400)
                time.sleep(0.5)
                led.off()
                buzzer.beep(0.2, 1200)
                time.sleep(0.5)






