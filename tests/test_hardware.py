import pytest
import sys
from unittest.mock import MagicMock

# Mock machine module for hardware tests is already setup in conftest.py
mock_machine = sys.modules['machine']

from hardware.led import StatusLED
from sensors.buzzer import Buzzer
from flight.controller import FlightController
from flight.states import FlightState

def test_status_led():
    mock_machine.Pin.reset_mock()
    led = StatusLED()
    mock_machine.Pin.assert_called()
    
    mock_pin_inst = mock_machine.Pin.return_value
    mock_pin_inst.reset_mock()
    
    led.on()
    mock_pin_inst.value.assert_called_with(1)
    
    led.off()
    mock_pin_inst.value.assert_called_with(0)
    
    mock_pin_inst.value.return_value = 0
    led.toggle()
    mock_pin_inst.value.assert_called_with(True)

def test_buzzer(monkeypatch):
    import time
    mock_sleep = MagicMock()
    monkeypatch.setattr(time, "sleep", mock_sleep)
    
    mock_machine.PWM.reset_mock()
    buzzer = Buzzer(15)
    mock_machine.PWM.assert_called()
    
    mock_pwm_inst = mock_machine.PWM.return_value
    mock_pwm_inst.reset_mock()
    
    buzzer.beep(0.1)
    mock_pwm_inst.duty_u16.assert_any_call(32768)
    mock_pwm_inst.duty_u16.assert_any_call(0)
    mock_sleep.assert_called_with(0.1)

def test_controller_with_real_hardware_classes(monkeypatch):
    # Tests that the FlightController works with instantiated Hardware components
    # The machine module is already mocked above, so the pins won't try to access real HW
    import time
    mock_sleep = MagicMock()
    monkeypatch.setattr(time, "sleep", mock_sleep)
    
    i2c = MagicMock()
    sensors = {
        'imu': MagicMock(),
        'bmp': MagicMock()
    }
    hardware = {
        'led': StatusLED(),
        'buzzer': Buzzer(15)
    }
    logger = MagicMock()
    telemetry = MagicMock()
    
    ticks = [0, 6000]
    def mock_ticks():
        return ticks.pop(0) if ticks else 6000
    
    monkeypatch.setattr(time, "ticks_ms", mock_ticks)
    
    sensors['imu'].read_acceleration.return_value = (0, 0, 9.81)
    sensors['bmp'].read_altitude.return_value = 0.0
    
    mock_machine.PWM.return_value.reset_mock()
    
    fc = FlightController(i2c, sensors, hardware, logger, telemetry)
    fc.update()
    
    assert fc.state == FlightState.ARMED
    # check that the real buzzer called down to the mocked PWM duty_u16
    mock_machine.PWM.return_value.duty_u16.assert_any_call(32768)
    mock_machine.PWM.return_value.duty_u16.assert_any_call(0)
