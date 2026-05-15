from machine import Pin, PWM
import time


class Buzzer:
    def __init__(self, pin_num):
        self.buzzer = PWM(Pin(pin_num))
        self.buzzer.duty_u16(0)

    def beep(self, duration=0.1, frequency=2000):
        self.buzzer.freq(frequency)

        self.buzzer.duty_u16(32768)

        time.sleep(duration)

        self.buzzer.duty_u16(0)

    def boot_beep(self):
        tones = [1000, 1500, 2000]

        for tone in tones:
            self.beep(0.1, tone)
            time.sleep(0.05)

    def error_beep(self, repeats=5):
        for _ in range(repeats):
            self.beep(0.5, 400)
            time.sleep(0.2)

    def success_beep(self):
        self.beep(0.1, 2500)
        time.sleep(0.05)
        self.beep(0.1, 3000)

    def stop(self):
        self.buzzer.deinit()