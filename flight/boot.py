from sensors.buzzer import Buzzer
from hardware.led import StatusLED


def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(15)

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