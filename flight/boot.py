from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from hardware.lcd_i2c import I2cLcd
from machine import I2C, Pin


def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(20) # GP-15

    led.on()

    try:
        print("PBFR VERSION 1")

        for _ in range(3):
            buzzer.beep()

        print("PBFR READY")

    except Exception as e:
        print("BOOT FAILURE:", e)

        while True:
            buzzer.beep(1.0)