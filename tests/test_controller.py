import pytest
from unittest.mock import MagicMock

from flight import watchdog
from flight.controller import FlightController, FlightState
from fakes.fakewatchdog import FakeWatchdog

@pytest.fixture
def mocks():
    sensors = {
        'imu': MagicMock(),
        'bmp': MagicMock()
    }
    hardware = {
        'led': MagicMock(),
        'buzzer': MagicMock()
    }
    logger = MagicMock()
    telemetry = MagicMock()
    i2c = MagicMock()
    return i2c, sensors, hardware, logger, telemetry

def test_initial_state(mocks):
    i2c, sensors, hardware, logger, telemetry = mocks
    fc = FlightController(i2c, sensors, hardware, logger, telemetry)
    assert fc.state == FlightState.IDLE

def test_transition_to_armed(mocks, monkeypatch):
    i2c, sensors, hardware, logger, telemetry = mocks
    
    # Mock time to progress
    ticks = [0, 6000] # 0ms at init, 6000ms at update
    def mock_ticks():
        return ticks.pop(0) if ticks else 6000
    
    monkeypatch.setattr("time.ticks_ms", mock_ticks)
    
    sensors['imu'].read_acceleration.return_value = (0, 0, 9.81)
    sensors['bmp'].read_altitude.return_value = 0.0
    
    fc = FlightController(i2c, sensors, hardware, logger, telemetry)
    fc.update()
    
    assert fc.state == FlightState.ARMED
    hardware['buzzer'].beep.assert_called()

def test_transition_to_powered_flight(mocks, monkeypatch):
    i2c, sensors, hardware, logger, telemetry = mocks
    
    # Start in ARMED state
    fc = FlightController(i2c, sensors, hardware, logger, telemetry)
    fc.state = FlightState.ARMED
    
    # Mock high acceleration
    sensors['imu'].read_acceleration.return_value = (0, 0, 20.0)
    sensors['bmp'].read_altitude.return_value = 10.0
    
    fc.update()
    
    assert fc.state == FlightState.POWERED_FLIGHT
