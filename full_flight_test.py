import pytest
from unittest.mock import MagicMock

from flight.controller import FlightController
from flight.states import FlightState

import sys

ON_PICO = sys.platform == "rp2"

@pytest.fixture
def mocks():
    sensors = {
        'imu': MagicMock(),
        'bmp': MagicMock()
    }
    logger = MagicMock()
    telemetry = MagicMock()
    i2c = MagicMock()
    return i2c, sensors, None, logger, telemetry

def create_hardware():
    if ON_PICO:
        from hardware.led import StatusLED
        from sensors.buzzer import Buzzer

        return {
            "led": StatusLED(),
            "buzzer": Buzzer(15),
        }

    return {
        "led": MagicMock(),
        "buzzer": MagicMock(),
    }


def test_full_flight(mocks):
    i2c, sensors, _, logger, telemetry = mocks

    # Use REAL hardware on Pico
    hardware = create_hardware()

    fc = FlightController(
        i2c,
        sensors,
        hardware,
        logger,
        telemetry
    )

    # Simulated acceleration profile
    sensors['imu'].read_acceleration.side_effect = [
        (0, 0, 9.81),   # idle -> armed
        (0, 0, 9.81),   # armed
        (0, 0, 22.0),   # launch
        (0, 0, 20.0),   # powered ascent
        (0, 0, 15.0),   # coast
        (0, 0, 9.81),   # apogee/descent
        (0, 0, 9.81),
        (0, 0, 9.81),
        (0, 0, 9.81),
    ] + [(0, 0, 9.81)] * 10

    # Simulated altitude profile
    sensors['bmp'].read_altitude.side_effect = [
        0,
        0,
        50,
        150,
        300,
        280,
        200,
        50,
        0
    ] + [0] * 10

    # Run simulated flight loop (15 checks needed to wait for landing condition to hit)
    for _ in range(15):
        fc.update()

    # Validate final state
    assert fc.state == FlightState.LANDED

    # Desktop-only mock assertions
    if not ON_PICO:
        hardware['buzzer'].beep.assert_called()