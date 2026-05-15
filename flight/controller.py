import time
from flight.states import FlightState


class FlightController:
    def __init__(self, i2c, sensors, hardware, logger, telemetry=None):
        self.i2c = i2c
        self.sensors = sensors
        self.hardware = hardware
        self.logger = logger
        self.telemetry = telemetry

        self.state = FlightState.IDLE
        try:
            self.init_time = time.ticks_ms()
        except AttributeError:
            # Fallback if ticks_ms is not available
            self.init_time = 0

        self.last_altitude = 0
        self.descent_counter = 0
        self.landed_counter = 0

    def boot(self):
        self.state = FlightState.READY
        self.emit("READY")

    def emit(self, event):
        if self.telemetry:
            self.telemetry.send(event)

    def update(self):
        ax, ay, az = self.sensors['imu'].read_acceleration()
        altitude = self.sensors['bmp'].read_altitude()

        if self.state == FlightState.IDLE:
            try:
                current_time = time.ticks_ms()
            except AttributeError:
                current_time = 5000
            
            if current_time - self.init_time >= 5000:
                self.setstate(FlightState.ARMED)

        # Launch detection
        elif self.state == FlightState.ARMED or self.state == FlightState.READY:
            if az > 15:
                print("LAUNCH!")
                self.setstate(FlightState.POWERED_FLIGHT)

        # Apogee detection
        elif self.state == FlightState.POWERED_FLIGHT or self.state == FlightState.ASCENT:
            if altitude < self.last_altitude:
                self.descent_counter += 1
            else:
                self.descent_counter = 0

            if self.descent_counter >= 3:
                print("APOGEE!")
                self.setstate(FlightState.APOGEE)

        # Descent
        elif self.state == FlightState.APOGEE:
            print("DESCENT!")
            self.setstate(FlightState.DESCENT)

        # Landing
        elif self.state == FlightState.DESCENT:
            if altitude < 5 and abs(az - 9.81) < 0.5:
                self.landed_counter += 1
            else:
                self.landed_counter = 0

            if self.landed_counter >= 5:
                print("LANDED!")
                self.setstate(FlightState.LANDED)

        self.last_altitude = altitude

    def setstate(self, new_state):
        self.state = new_state

        event = "READY"
        if new_state == FlightState.ARMED:
            event = "ARMED"
        elif new_state == FlightState.POWERED_FLIGHT:
            event = "LAUNCH"
        elif new_state == FlightState.APOGEE:
            event = "APOGEE"
        elif new_state == FlightState.DESCENT:
            event = "DESCENT"
        elif new_state == FlightState.LANDED:
            event = "LANDED"
            
        self.emit(event)

        buzzer = self.hardware.get('buzzer')
        if not buzzer:
            return

        if new_state == FlightState.ARMED:
            buzzer.beep(0.1, 1000)
        elif new_state == FlightState.POWERED_FLIGHT:
            buzzer.beep(0.2, 2000)
        elif new_state == FlightState.APOGEE:
            buzzer.beep(0.3, 1400)
        elif new_state == FlightState.DESCENT:
            buzzer.beep(1, 1500)
        elif new_state == FlightState.LANDED:
            # We don't want a blocking while loop here, otherwise update loop hangs
            buzzer.beep(1, 800)