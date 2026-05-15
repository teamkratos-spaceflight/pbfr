from sensors.buzzer import Buzzer
from sensors.bmp280 import BMP280
from hardware.led import StatusLED
from machine import I2C, Pin


def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(20) # GP-15
    bmp=BMP280(BMP280)
    
    # Initialize I2C
    try:
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    except Exception as e:
        print("I2C Init Failed:", e)
        i2c = None

    led.on()

    try:
        print("PBFR VERSION 1")
        print("Running self test...")
        bmp.boot_test()

        for _ in range(3):
            buzzer.beep()

        print("PBFR READY")
            
        return i2c

    except Exception as e:
        print("BOOT FAILURE:", e)

        while True:
            buzzer.beep(1.0)