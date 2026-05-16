class ValidationResult:
    def __init__(self, valid=True, fault=None):
        self.valid = valid
        self.fault = fault


class SensorValidator:
    def __init__(self):
        self.last_altitude = None
        self.last_acceleration = None

    # IMU VALIDATION

    def validate_acceleration(self, accel):
        try:
            ax, ay, az = accel
        except Exception:
            return ValidationResult(
                False,
                "IMU returned malformed acceleration"
            )

        # Impossible acceleration check
        if abs(ax) > 100 or abs(ay) > 100 or abs(az) > 100:
            return ValidationResult(
                False,
                "IMU acceleration out of range"
            )

        # Frozen sensor detection
        if accel == self.last_acceleration:
            return ValidationResult(
                False,
                "IMU acceleration frozen"
            )

        self.last_acceleration = accel

        return ValidationResult(True)

    # BAROMETER VALIDATION

    def validate_altitude(self, altitude):
        if altitude is None:
            return ValidationResult(
                False,
                "BMP280 returned None altitude"
            )

        if altitude < -100 or altitude > 10000:
            return ValidationResult(
                False,
                "BMP280 altitude out of range"
            )

        # Teleportation check
        if self.last_altitude is not None:
            delta = abs(altitude - self.last_altitude)

            if delta > 1000:
                return ValidationResult(
                    False,
                    "Altitude jump too large"
                )

        self.last_altitude = altitude

        return ValidationResult(True)