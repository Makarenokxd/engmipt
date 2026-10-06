import smbus
import RPi.GPIO as GPIO

dynamic_range = 5.11
class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF

        self.bus.write_byte_data(
            self.address,
            first_byte,
            second_byte
        )

        if self.verbose:
            print(
                f"Число: {number}, отправленные по I2C данные: "
                f"[0x{(self.address << 1):02X}, "
                f"0x{first_byte:02X}, "
                f"0x{second_byte:02X}]\n"
            )

    def set_voltage(self, voltage):
        if not (0 <= voltage <= self.dynamic_range):
            print("Напряжение выходит за динамический диапазон ЦАП")
            return

        number = round(voltage / self.dynamic_range * 4095)

        self.set_number(number)


if __name__ == "__main__":
    dac = MCP4725(5.11)

    while True:
        try:
            voltage = float(input("Введите напряжение в вольтах :"))

            if 0 <= voltage <= dac.dynamic_range:
                dac.set_voltage(voltage)
            else:
                print(
                    f"Напряжение выходит за динамический диапазон"
                    f"ЦАП (0.00 - {dac.dynamic_range:.2f} B"
                )
            
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз")
    dac.deinit()