import bluetooth
import struct
import time

class BLESender:
    def __init__(self, name="PBFR"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)

        self.name = name

        # simple UART-like service (common pattern)
        self._init_ble()

    def _init_ble(self):
        # minimal UART service UUIDs
        UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

        TX_CHAR = (TX_UUID, bluetooth.FLAG_NOTIFY)

        UART_SERVICE = (UART_UUID, (TX_CHAR,))

        ((self.tx_handle,),) = self.ble.gatts_register_services((UART_SERVICE,))

        self.connections = set()

        def irq(event, data):
            if event == 1:
                self.connections.add(data[0])
            elif event == 2:
                self.connections.remove(data[0])

        self.ble.irq(irq)

    def send(self, msg):
        try:
            for conn in self.connections:
                self.ble.gatts_notify(conn, self.tx_handle, msg)
        except:
            pass