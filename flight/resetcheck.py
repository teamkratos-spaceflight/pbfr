import machine

class ResetChecker:
    CAUSES = {
        0: "POWER_ON",
        1: "HARD_RESET",
        2: "WDT_RESET",
        3: "DEEPSLEEP",
        4: "SOFT_RESET"
    }

    @staticmethod
    def get_cause():
        cause = machine.reset_cause()

        return ResetChecker.CAUSES.get(cause, f"UNKNOWN({cause})")


    @staticmethod
    def watchdog_triggered():
        return machine.reset_cause() == 2