from sensors.imu import IMU
from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from hardware.sdcard import SDLogger
from sensors.bmp280 import BMP280
from flight.boot import boot_sequence
from telemetry.blemetry import BLESender
import time

print("PBFR: Starting Main Application")

i2c, lcd = boot_sequence()

imu = IMU(i2c)
led = StatusLED()
log = SDLogger()
send = BLESender()
log.start()

print("PBFR: Entering Main Loop")

t0 = time.ticks_ms()

while True:
    t = (time.ticks_ms() - t0) / 1000

    accel = imu.read_acceleration()

    log.log(t, accel[0], accel[1], accel[2])

    if lcd:
        lcd.move_to(0, 0)
        lcd.putstr("PBFR ACTIVE")

        lcd.move_to(0, 1)
        lcd.putstr("AX:{:.2f}".format(accel[0]))

    print("Accel:", accel)

    led.toggle()
    time.sleep(1.0)