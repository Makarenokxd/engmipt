import mcp4725_driver as mcp
import signal_generator as sg
import time

# ---------- параметры сигнала ----------
amplitude = 5.10           # В (чуть меньше dynamic_range = 5.11 В)
signal_frequency = 10      # Гц
sampling_frequency = 1000  # Гц (100 точек на период)

# ---------- основная программа ----------
try:
    dac = mcp.MCP4725(
        dynamic_range=5.11,
        address=0x61,
        verbose=False,
    )

    start_time = time.perf_counter()
    next_sample_time = start_time

    while True:
        # Ждём точного момента выборки
        next_sample_time = sg.wait_for_sampling_period(
            sampling_frequency, next_sample_time
        )

        t = next_sample_time - start_time
        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = norm_amp * amplitude
        dac.set_voltage(voltage)

finally:
    dac.deinit()
