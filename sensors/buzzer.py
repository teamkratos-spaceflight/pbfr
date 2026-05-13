from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin_num):
        self.buzzer = PWM(Pin(pin_num))

    def beep(self, freq=1000, duration=0.2):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(37268)

        time.sleep(duration)

        self.buzzer.duty_u16(0)