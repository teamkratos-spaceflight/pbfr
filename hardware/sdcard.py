class SDLogger:
    def __init__(self):
        self.file = None

    def start(self):
        self.file = open("flight.csv", "w")
        self.file.write("t,ax,ay,az\n")

    def log(self, t, ax, ay, az):
        if self.file:
            self.file.write(f"{t},{ax},{ay},{az}\n")

    def close(self):
        if self.file:
            self.file.close()