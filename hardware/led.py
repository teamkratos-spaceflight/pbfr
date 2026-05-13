from machine import Pin

class StatusLED:
    def __init__(self):
        try:
            self.led = Pin("LED", Pin.OUT)
        except (ValueError, TypeError):
            # Fallback to a common pin like 25 (Pico) if "LED" fails
            try:
                self.led = Pin(25, Pin.OUT)
            except:
                self.led = None
                print("LED: Could not initialize LED pin")

    def on(self):
        if self.led:
            self.led.value(1)

    def off(self):
        if self.led:
            self.led.value(0)

    def toggle(self):
        self.led.value(not self.led.value())