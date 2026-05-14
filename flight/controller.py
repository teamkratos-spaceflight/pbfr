from flight.states import FlightState


class FlightController:
    def __init__(self, imu, barometer, telemetry=None):
        self.imu = imu
        self.barometer = barometer
        self.telemetry = telemetry

        self.state = FlightState.BOOT

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
        ax, ay, az = self.imu.read_acceleration()
        altitude = self.barometer.read_altitude()

        # Launch detection
        if self.state == FlightState.READY:
            if az > 15:
                self.state = FlightState.ASCENT
                self.emit("LAUNCH")

        # Apogee detection
        elif self.state == FlightState.ASCENT:
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