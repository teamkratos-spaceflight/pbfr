from flight.controller import FlightController
from flight.states import FlightState
import sys

ON_PICO = sys.platform == "rp2"

def test_full_flight(mocks):
    i2c, sensors, hardware, logger, telemetry = mocks

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
    ]

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
    ]

    # Run simulated flight loop
    for _ in range(9):
        fc.update()

    # Validate final state
    assert fc.state == FlightState.LANDED