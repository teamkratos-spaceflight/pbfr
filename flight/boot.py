from hardware.buzzer_diag import test_pin
from sensors.buzzer import Buzzer
from sensors.bmp280 import BMP280
from hardware.led import StatusLED
from hardware.sdcard import SDLogger
from sensors.imu import IMU
from machine import I2C, Pin
import hardware.buzzer_diag
from flight.scenarios.full_flight import run
from flight.controller import FlightController

import time



def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(15) # GP-15
    imu = IMU(I2C)
    bmp = BMP280(BMP280)
    sd = SDLogger()



    
    # Initialize I2C
    try:
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    except Exception as e:
        print("I2C Init Failed:", e)
        i2c = None

    led.on()

    try:
        print("Welcome to PBFR 1!")
        print("Running self test...")
        bmp.boot_test()
        time.sleep(1)
        imu.boot_test()
        time.sleep(1)
        sd.boot_test()
        time.sleep(1)

        print("PBFR READY")

        imu = IMU(None)
        bmp = BMP280(None)

        fc = FlightController(
            i2c=None,
            sensors={"imu": imu, "bmp": bmp},
            hardware={
                "led": StatusLED(),
                "buzzer": Buzzer(15)
            },
            logger=None,
            telemetry=None
        )

        print("RUNNING FULL FLIGHT SCENARIO")

        run(fc)
        
        # After full scenario, don't trap into an infinite loop so boot sequence can complete
        
        return i2c

    except Exception as e:
        print("BOOT FAILURE:", e)

        while True:
            buzzer.beep(1.0)