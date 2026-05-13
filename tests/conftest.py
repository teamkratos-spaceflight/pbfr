import sys
from unittest.mock import MagicMock

# Mock Micropython modules
mock_machine = MagicMock()
mock_bluetooth = MagicMock()
mock_utime = MagicMock()

# Setup time mocks
mock_utime.ticks_ms.side_effect = lambda: int(0) # Will be overridden in tests

sys.modules['machine'] = mock_machine
sys.modules['bluetooth'] = mock_bluetooth
sys.modules['utime'] = mock_utime
sys.modules['time'] = mock_utime # In Micropython time and utime are often similar

# Additional common Micropython modules
sys.modules['micropython'] = MagicMock()
sys.modules['network'] = MagicMock()
sys.modules['ubinascii'] = MagicMock()
