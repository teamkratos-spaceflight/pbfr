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
                self.state = FlightState.ARMED
                self.emit("ARMED")
                if 'buzzer' in self.hardware and self.hardware['buzzer']:
                    self.hardware['buzzer'].beep()

        # Launch detection
        elif self.state == FlightState.ARMED or self.state == FlightState.READY:
            if az > 15:
                self.state = FlightState.POWERED_FLIGHT
                self.emit("LAUNCH")

        # Apogee detection
        elif self.state == FlightState.POWERED_FLIGHT or self.state == FlightState.ASCENT:
            if altitude < self.last_altitude:
                self.descent_counter += 1
            else:
                self.descent_counter = 0

            if self.descent_counter >= 3:
                self.state = FlightState.APOGEE
                self.emit("APOGEE")

        # Descent
        elif self.state == FlightState.APOGEE:
            self.state = FlightState.DESCENT
            self.emit("DESCENT")

        # Landing
        elif self.state == FlightState.DESCENT:
            if altitude < 5 and abs(az - 9.81) < 0.5:
                self.landed_counter += 1
            else:
                self.landed_counter = 0

            if self.landed_counter >= 5:
                self.state = FlightState.LANDED
                self.emit("LANDED")

        self.last_altitude = altitude