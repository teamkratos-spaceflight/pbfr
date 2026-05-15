from flight.states import FlightState
from hardware.buzzer import Buzzer
from sensors.bmp280 import BMP280
from hardware.led import StatusLED
from hardware.sdcard import SDLogger
from sensors.imu import IMU
from machine import I2C, Pin
# import hardware.buzzer_diag
from flight.resetcheck import ResetChecker
from flight.controller import FlightController

import time



def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(15) # GP-15
    imu = IMU(I2C)
    bmp = BMP280(BMP280)
    sd = SDLogger()
    fc = FlightController()



    
    # Initialize I2C
    try:
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    except Exception as e:
        print("I2C Init Failed:", e)
        i2c = None

    led.on()

    try:
        print("Welcome to PBFR 1!")
        if ResetChecker.watchdog_triggered():
            print("BOOT HALT: LOC-F!")
            fc.setstate(FlightState.LOC_F)
            buzzer.beep(1.0, 1200)

        print("Running self test...")
        bmp.boot_test()
        time.sleep(1)
        imu.boot_test()
        time.sleep(1)
        sd.boot_test()
        time.sleep(1)

        print("PBFR READY")

        
        return i2c

    except Exception as e:
        print("BOOT FAILURE:", e)

        while True:
            buzzer.beep(1.0)