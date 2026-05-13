from sensors.buzzer import Buzzer
from hardware.led import StatusLED
from hardware.lcd_i2c import I2cLcd
from machine import I2C, Pin


def boot_sequence():
    led = StatusLED()
    buzzer = Buzzer(20) # GP-15
    
    # Initialize I2C and LCD
    try:
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        # Scan for LCD (usually 0x27 or 0x3f)
        devices = i2c.scan()
        lcd_addr = 0x27
        if 0x3f in devices: lcd_addr = 0x3f
        elif 0x27 not in devices and devices: lcd_addr = devices[0]
        
        lcd = I2cLcd(i2c, lcd_addr, 4, 20)
        lcd.putstr("PBFR SYSTEM BOOTING")
    except Exception as e:
        print("LCD/I2C Init Failed:", e)
        i2c = None
        lcd = None

    led.on()

    try:
        print("PBFR VERSION 1")
        if lcd:
            lcd.move_to(0, 1)
            lcd.putstr("VERSION 1.0")

        for _ in range(3):
            buzzer.beep()

        print("PBFR READY")
        if lcd:
            lcd.move_to(0, 2)
            lcd.putstr("STATUS: READY")
            
        return i2c, lcd

    except Exception as e:
        print("BOOT FAILURE:", e)
        if lcd:
            lcd.clear()
            lcd.putstr("BOOT FAILURE")

        while True:
            buzzer.beep(1.0)