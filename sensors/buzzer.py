from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin_num):
        self.buzzer = PWM(Pin(pin_num), freq=2000)

    def beep(self, duration=0.1):
        print("Buzzer: Beep starting...")
        self.buzzer.duty_u16(32768)
        time.sleep(duration)
        self.buzzer.duty_u16(0)
        print("Buzzer: Beep ended")

    def boot_beep(self):
        for _ in range(3):
            self.beep(0.1)
            time.sleep(0.1)

    def error_beep(self):
        while True:
            self.beep(0.5)
            time.sleep(0.5)