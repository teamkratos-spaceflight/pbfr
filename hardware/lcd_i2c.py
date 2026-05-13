import time
from machine import I2C, Pin

# LCD Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = LCD_BACKLIGHT
        self.display_function = LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS
        self.display_control = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display_mode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        
        # Initialization sequence
        time.sleep(0.05)
        self.write_four_bits(0x03 << 4)
        time.sleep(0.005)
        self.write_four_bits(0x03 << 4)
        time.sleep(0.005)
        self.write_four_bits(0x03 << 4)
        self.write_four_bits(0x02 << 4)
        
        self.command(LCD_FUNCTIONSET | self.display_function)
        self.command(LCD_DISPLAYCONTROL | self.display_control)
        self.command(LCD_CLEARDISPLAY)
        self.command(LCD_ENTRYMODESET | self.display_mode)
        time.sleep(0.2)

    def write_four_bits(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight]))
        self.strobe(data)

    def strobe(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | En | self.backlight]))
        time.sleep(0.0005)
        self.i2c.writeto(self.i2c_addr, bytes([(data & ~En) | self.backlight]))
        time.sleep(0.0001)

    def send(self, data, mode):
        self.write_four_bits(mode | (data & 0xF0))
        self.write_four_bits(mode | ((data << 4) & 0xF0))

    def command(self, value):
        self.send(value, 0)

    def write(self, value):
        self.send(value, Rs)

    def clear(self):
        self.command(LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def home(self):
        self.command(LCD_RETURNHOME)
        time.sleep(0.002)

    def move_to(self, cursor_x, cursor_y):
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += 20  # For 20x4
        self.command(LCD_SETDDRAMADDR | addr)

    def putstr(self, string):
        for char in string:
            self.write(ord(char))

    def backlight_on(self):
        self.backlight = LCD_BACKLIGHT
        self.command(0)

    def backlight_off(self):
        self.backlight = LCD_NOBACKLIGHT
        self.command(0)
