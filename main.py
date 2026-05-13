from sensors.imu import IMU
from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from flight.boot import boot_sequence
import time

print("PBFR: Starting Main Application")

# Run boot sequence first
i2c, lcd = boot_sequence()

# Initialize IMU with actual I2C if available
imu = IMU(i2c)
led = StatusLED()

print("PBFR: Entering Main Loop")

if lcd:
    time.sleep(1)
    lcd.clear()
    lcd.putstr("PBFR ACTIVE")

while True:
    accel = imu.read_acceleration()
    
    if lcd:
        lcd.move_to(0, 1)
        lcd.putstr(f"AX:{accel[0]:>5.2f} AY:{accel[1]:>5.2f}")
        lcd.move_to(0, 2)
        lcd.putstr(f"AZ:{accel[2]:>5.2f}")
    
    print("Accel:", accel)
    led.toggle()
    
    time.sleep(1.0)
