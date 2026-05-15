class FakeWatchdog:
    def __init__(self):
        self.kicked = 0

    def kick(self):
        self.kicked += 1