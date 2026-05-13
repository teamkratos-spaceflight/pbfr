from sensors.imu import IMU
from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from flight.boot import boot_sequence

print("PBFR: Starting Main Application")

# Run boot sequence first
boot_sequence()

imu = IMU(None)
led = StatusLED()

print("PBFR: Entering Main Loop")

while True:
    print("PBFR: Reading IMU...")
    accel = imu.read_acceleration()
    print("Accel:", accel)
    
    led.toggle()
    
    # Just a short beep occasionally to prove it works
    # buzzer.beep(0.05) 
    
    import time
    time.sleep(2.0)
