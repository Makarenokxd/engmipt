import smbus
import time


class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Данные: {data}, старший: {upper_data_byte:x}, младший: {lower_data_byte:x}, число: {number}")
        return number

    def get_voltage(self):
        return self.get_number() / 1024 * self.dynamic_range


if __name__ == "__main__":
    adc = MCP3021(5.11)
    try:
        while True:
            print(f"{adc.get_voltage():.3f} В")
            time.sleep(1)
    finally:
        adc.deinit()
