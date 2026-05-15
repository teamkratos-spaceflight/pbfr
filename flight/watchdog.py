from machine import WDT

class Watchdog:
    def __init__(self, timeout_ms=3000):
        self._wdt = WDT(timeout=timeout_ms)
        self._timeout_ms = timeout_ms
        print(f"Watchdog armed! ({timeout_ms}) ms")

    def kick(self):
        """Feed the watchdog to prevent reset"""
        self._wdt.feed()

    def reset(self):
        """Alias for clarity in flight mode"""
        self.kick()

    def status(self):
        return {
            "timeout_ms": self._timeout_ms
        }
