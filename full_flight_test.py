import pytest
from unittest.mock import MagicMock, cast

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
        from hardware.buzzer import Buzzer

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
        (0, 0, 9.81),
        (0, 0, 9.81),
        (0, 0, 22.0),
        (0, 0, 20.0),
        (0, 0, 15.0),
        (0, 0, 9.81),
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

    # Run simulated flight loop
    for _ in range(15):
        fc.update()

    # Final state check
    assert fc.state == FlightState.LANDED

    # Desktop-only mock assertions
    if not ON_PICO:
        buzzer_mock = cast(MagicMock, hardware["buzzer"])

        buzzer_mock.beep.assert_called()