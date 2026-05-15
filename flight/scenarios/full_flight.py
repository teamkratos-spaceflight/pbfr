from flight.states import FlightState


def run(fc):
    accel_data = [
        (0, 0, 9.81),
        (0, 0, 9.81),
        (0, 0, 22.0),
        (0, 0, 20.0),
        (0, 0, 15.0),
        (0, 0, 9.81),
        (0, 0, 9.81),
        (0, 0, 9.81),
    ] + [(0, 0, 9.81)] * 10

    alt_data = [
        0, 0, 50, 150, 300, 280, 200, 50, 0
    ] + [0] * 10
    
    def read_accel():
        if accel_data:
            return accel_data.pop(0)
        return (0, 0, 9.81)
        
    def read_alt():
        if alt_data:
            return alt_data.pop(0)
        return 0
        
    fc.sensors['imu'].read_acceleration = read_accel
    fc.sensors['bmp'].read_altitude = read_alt

    for _ in range(15):
        fc.update()

    return fc.state