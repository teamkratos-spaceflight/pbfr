import telemetry
from sensors.imu import IMU
from hardware.led import StatusLED
from hardware.sdcard import SDLogger
from sensors.bmp280 import BMP280
from hardware.buzzer import Buzzer
from flight.boot import boot_sequence
from flight.watchdog import Watchdog
from telemetry.blemetry import BLESender
import time


from flight.controller import FlightController

i2c = boot_sequence()

MELODY = [
    (1000, 0.1),
    (1500, 0.1),
    (2000, 0.2),
]

# Sensors
imu = IMU(i2c)
bmp = BMP280(i2c)

# Hardware components
led = StatusLED()
buzzer = Buzzer(15)

# Services
log = SDLogger()
send = BLESender()
watchdog = Watchdog(timeout_ms=3000)

log.start()

# Initialize Controller
sensors = {'imu': imu, 'bmp': bmp}
hardware = {'led': led, 'buzzer': buzzer}

fc = FlightController(i2c, sensors, hardware, log, send)

print("PBFR: Entering Main Loop")

for freq, dur in MELODY:
    buzzer.beep(dur, freq)

while True:
    fc.update()
    time.sleep(0.05)
    watchdog.kick()
    time.sleep(0.05)