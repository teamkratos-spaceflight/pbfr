import time
from hardware.led import StatusLED
from hardware.buzzer import Buzzer

class BMP280:
    def __init__(self, i2c):
        self.i2c = i2c
        self.address = 0x77

    def read_pressure(self):
        # placeholder until driver is added
        return 1013.25

    def read_altitude(self):
        # simple fake altitude model for now
        return 0.0

    def boot_test(self):
        led = StatusLED()
        buzzer = Buzzer(15) # means Pin 15. ALWAYS USE PIN 15!! (PHYSICAL PIN 20)!!!
        led.toggle()
        print("## BMP280 BOOT TEST ##")
        buzzer.beep(0.1, 3000)
        print("BMP280 pressure read test...")
        self.read_pressure()
        if self.read_pressure() < 1:
            pressure = self.read_pressure()
            print("!!! BMP280 pressure read test failed !!!")
            print(f"Test failed at: {pressure} when pressure is {pressure*100}%")
            print("! BMP FAILURE !")
            while True:
                led.toggle()
                buzzer.beep(0.2, 400)
                time.sleep(0.5)
                buzzer.beep(0.2, 1200)
                led.toggle()
                time.sleep(0.5)

        print("BMP280 pressure read test passed")

        print("BMP280 altitude read test...")
        self.read_altitude()
        if self.read_altitude() > 1:
            print("BMP280 altitude read test failed")
            print("BMP FAILURE!")
            while True:
                led.toggle()
                buzzer.beep()
                time.sleep(1)
                led.toggle()
                buzzer.beep()
        print("BMP280 altitude read test passed")
        print("BMP280 PASSED")


