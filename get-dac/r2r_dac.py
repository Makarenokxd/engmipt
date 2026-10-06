import RPi.GPIO as GPIO


class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not (0 <= number <= 255):
            if self.verbose:
                print("Число выходит за диапазон ЦАП (0 - 255)")
            return

        for i in range(8):
            GPIO.output(self.gpio_bits[i], (number >> i) & 1)

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(
                    f"Напряжение выходит за динамический диапазон "
                    f"ЦАП (0.00 - {self.dynamic_range:.2f} В)"
                )
                print("Устанавливаем 0.0 В")

            self.set_number(0)
            return

        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = R2R_DAC([22, 27, 17, 26, 25, 21, 20, 16], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()