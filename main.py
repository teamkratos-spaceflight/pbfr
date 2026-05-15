from sensors.imu import IMU
from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from hardware.sdcard import SDLogger
from sensors.bmp280 import BMP280
from sensors.buzzer import Buzzer
from flight.boot import boot_sequence
from telemetry.blemetry import BLESender
import time

print("PBFR: Starting Main Application")

from flight.controller import FlightController

i2c = boot_sequence()

# Sensors
imu = IMU(i2c)
bmp = BMP280(i2c)

# Hardware components
led = StatusLED()
buzzer = Buzzer(20)

# Services
log = SDLogger()
send = BLESender()

log.start()

# Initialize Controller
sensors = {'imu': imu, 'bmp': bmp}
hardware = {'led': led, 'buzzer': buzzer}

fc = FlightController(i2c, sensors, hardware, log, send)

print("PBFR: Entering Main Loop")
while True:
    fc.update()
    time.sleep(0.05)