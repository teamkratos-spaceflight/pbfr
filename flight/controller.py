import time

class FlightState:
    IDLE = "IDLE"
    ARMED = "ARMED"
    POWERED_FLIGHT = "POWERED_FLIGHT"
    COAST = "COAST"
    RECOVERY = "RECOVERY"
    LANDED = "LANDED"

class FlightController:
    def __init__(self, i2c, sensors, hardware, logger, telemetry):
        self.i2c = i2c
        self.imu = sensors.get('imu')
        self.bmp = sensors.get('bmp')
        self.led = hardware.get('led')
        self.buzzer = hardware.get('buzzer')
        self.log = logger
        self.send = telemetry
        
        self.state = FlightState.IDLE
        self.start_time = time.ticks_ms()
        self.last_tick = self.start_time

    def get_time(self):
        return (time.ticks_ms() - self.start_time) / 1000

    def update(self):
        t = self.get_time()
        
        # Read sensors
        accel = self.imu.read_acceleration()
        alt = self.bmp.read_altitude()
        
        # Log data
        self.log.log(t, accel[0], accel[1], accel[2])
        
        # Telemetry
        # msg = f"{t:.2f},{self.state},{accel[0]:.2f},{alt:.2f}"
        # self.send.send(msg)
        
        # State transitions (simplified logic for now)
        if self.state == FlightState.IDLE:
            if t > 5: # Mock auto-arm
                self.state = FlightState.ARMED
                print(f"[{t:.2f}] STATE: ARMED")
                self.buzzer.beep()

        elif self.state == FlightState.ARMED:
            if accel[2] > 15: # Detected launch
                self.state = FlightState.POWERED_FLIGHT
                print(f"[{t:.2f}] STATE: POWERED_FLIGHT")

        elif self.state == FlightState.POWERED_FLIGHT:
            if accel[2] < 2: # Engine burnout / coast
                self.state = FlightState.COAST
                print(f"[{t:.2f}] STATE: COAST")

        # ... further state logic would go here

        # Feedback
        self.led.toggle()

    def run(self):
        print(f"Flight Controller Started in state: {self.state}")
        while True:
            self.update()
            time.sleep(0.1)
