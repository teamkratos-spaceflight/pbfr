# PBFR: Python Based firmware for amateur Rocketry 

PBFR is a lightweight, robust flight computer application designed for the Raspberry Pi Pico W. It handles sensor data acquisition, logging, telemetry, and autonomous state transitions during flight.

## Core Features

- **Autonomous Flight Logic**: State machine handling IDLE, ARMED, POWERED_FLIGHT, COAST, RECOVERY, and LANDED states.
- **Sensor Integration**: Interfaces with IMU and Barometric sensors for real-time telemetry.
- **Hardware Feedback**: Built-in support for LCD status displays, buzzers, and LEDs.
- **Data Logging**: Robust logging system to capture flight data for post-flight analysis.

## Getting Started

### Hardware Setup
Refer to [HARDWARE.md](HARDWARE.md) for detailed wiring instructions and pinout information.

### Software Installation
1. Flash your Raspberry Pi Pico W with the latest MicroPython firmware.
2. Upload the `flight/`, `sensors/`, `hardware/`, and `telemetry/` directories to the Pico.
3. Upload `main.py` to the root of the Pico.

## Development and Testing

This project uses `pytest` for automated testing.

### Prerequisites
- Python 3.10+
- `pytest`
- `pytest-mock`

### Running Tests
To run the test suite, execute the following command from the root directory:

```bash
pytest tests/
```

The tests are configured via `pyproject.toml` to automatically include the project root in the Python path.

## License
MIT
