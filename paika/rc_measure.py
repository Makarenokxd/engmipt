# Зарядка и разрядка RC-цепи на плате AUX.
# Цепь питается от GPIO14: 1 -> конденсатор заряжается, 0 -> разряжается.
# Напряжение на конденсаторе (SIG) меряет MCP3021 по I2C.
# Перед запуском: raspi-gpio set 2 a0 и raspi-gpio set 3 a0
import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.11      # В, динамический диапазон MCP3021 (как в задании про I2C АЦП)
PIN = 14                  # GPIO, от которого питается RC-цепь
CHARGE_TIME = 3           # с, сколько держим GPIO14 = 1
DISCHARGE_TIME = 3        # с, сколько держим GPIO14 = 0
CYCLES = 2                # сколько раз повторить зарядку + разрядку
FILE_NAME = "rc_data.csv"

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
adc = MCP3021(DYNAMIC_RANGE)
times, voltages = [], []


def record(duration, start):
    t_end = time.time() + duration
    while time.time() < t_end:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)


try:
    print("Разряжаю конденсатор перед началом...")
    time.sleep(1)
    start = time.time()
    for i in range(CYCLES):
        print(f"Цикл {i + 1}: зарядка")
        GPIO.output(PIN, 1)
        record(CHARGE_TIME, start)
        print(f"Цикл {i + 1}: разрядка")
        GPIO.output(PIN, 0)
        record(DISCHARGE_TIME, start)
finally:
    GPIO.output(PIN, 0)
    GPIO.cleanup()
    adc.deinit()

with open(FILE_NAME, "w") as f:
    f.write("time_s,voltage_V\n")
    for t, v in zip(times, voltages):
        f.write(f"{t:.6f},{v:.4f}\n")

print(f"Измерений: {len(times)}, частота ~{len(times) / times[-1]:.0f} Гц, сохранено в {FILE_NAME}")
