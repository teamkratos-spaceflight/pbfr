from sensors.imu import IMU
from sensors.buzzer import Buzzer

imu = IMU(None)
buzzer = Buzzer(15)

print(imu.read_acceleration())
buzzer.beep()