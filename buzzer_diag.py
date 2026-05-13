from machine import Pin, PWM
import time

PINS_TO_TEST = [15, 14, 13, 16, 18]

def test_pin(pin_num):
    print(f"\n--- Testing Pin {pin_num} ---")
    
    # 1. Test as Active Buzzer
    print(f"Pin {pin_num}: Testing as ACTIVE buzzer (Constant High)...")
    p = Pin(pin_num, Pin.OUT)
    p.value(1)
    time.sleep(0.5)
    p.value(0)
    time.sleep(0.5)
    
    # 2. Test as Passive Buzzer (Sweep frequencies)
    print(f"Pin {pin_num}: Testing as PASSIVE buzzer (PWM Sweep)...")
    try:
        pwm = PWM(Pin(pin_num))
        for freq in [500, 1000, 2000, 4000]:
            print(f"  Frequency: {freq}Hz")
            pwm.freq(freq)
            pwm.duty_u16(32768)
            time.sleep(0.3)
            pwm.duty_u16(0)
            time.sleep(0.1)
        pwm.deinit()
    except Exception as e:
        print(f"  PWM Error on Pin {pin_num}: {e}")

print("STARTING BUZZER DIAGNOSTICS")
print("Listen carefully for any sound.")

for pin in PINS_TO_TEST:
    test_pin(pin)

print("\nDIAGNOSTICS COMPLETE")
