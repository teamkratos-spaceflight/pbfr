# PBFR Hardware Connection Guide

This document outlines the wiring for the Raspberry Pi Pico W components used in this project.

## Components and Pinout

| Component | Pico Pin (Function) | Physical Pin | Notes |
| :--- | :--- | :--- | :--- |
| **Buzzer** | GP15 (PWM) | 20 | Pass `20` to the `Buzzer` constructor. |
| **I2C LCD** (SDA) | GP0 (I2C0 SDA) | 1 | Connect to SDA on the LCD backpack. |
| **I2C LCD** (SCL) | GP1 (I2C0 SCL) | 2 | Connect to SCL on the LCD backpack. |
| **Status LED** | GPIO 25 (Internal) | N/A | Labeled as `LED` in software. |

## Detailed Wiring

### I2C LCD Module (2004 with I2C Backpack)
1. **GND**: Connect to any GND pin on the Pico (e.g., Physical Pin 3, 8, 13, 18, 23, 28, 33, or 38).
2. **VCC**: Connect to **VBUS** (Physical Pin 40) if using a 5V LCD, or **3V3(OUT)** (Physical Pin 36) if and only if your LCD is 3.3V compatible. *Most Freenove LCDs require 5V (VBUS).*
3. **SDA**: Connect to **GP0** (Physical Pin 1).
4. **SCL**: Connect to **GP1** (Physical Pin 2).

### Buzzer
1. **Positive (+)**: Connect to **GP15** (Physical Pin 20).
2. **Negative (-)**: Connect to any **GND** pin.

### Status LED
- The code attempts to use the built-in LED (GPIO 25). No external wiring is required for the basic status indicator.

---

## Software Configuration
The I2C bus is initialized with:
```python
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
```
The LCD address is automatically detected (usually `0x27` or `0x3F`).
