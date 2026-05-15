import machine

class ResetChecker:
    WDT_RESET = 3

    @staticmethod
    def watchdog_triggered():
        return machine.reset_cause() == ResetChecker.WDT_RESET