# Запись напряжения на конденсаторе RC-цепи (вход SIG платы AUX) через MCP3021.
# Пока идёт запись: вставь разъём / отпусти кнопку S1 (зарядка),
# зажми кнопку S1 (разрядка). Повтори 2-3 раза.
import time
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.11      # В, напряжение на PWR блока AUX (уточни мультиметром)
DURATION = 15             # с, длительность записи
FILE_NAME = "rc_data.csv"

adc = MCP3021(DYNAMIC_RANGE)
times, voltages = [], []
try:
    print(f"Запись {DURATION} с...")
    start = time.time()
    while time.time() - start < DURATION:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)
finally:
    adc.deinit()

with open(FILE_NAME, "w") as f:
    f.write("time_s,voltage_V\n")
    for t, v in zip(times, voltages):
        f.write(f"{t:.6f},{v:.4f}\n")

print(f"Измерений: {len(times)}, частота ~{len(times) / DURATION:.0f} Гц, сохранено в {FILE_NAME}")
