import r2r_dac as r2r
import signal_generator as sg
import time

# ---------- параметры сигнала ----------
amplitude = 3.18           # В (чуть меньше dynamic_range = 3.183 В)
signal_frequency = 10      # Гц
sampling_frequency = 2000  # Гц (200 точек на период)

# ---------- основная программа ----------
try:
    dac = r2r.R2R_DAC(
        gpio_bits=[16, 20, 21, 25, 26, 17, 27, 22],
        dynamic_range=3.183,
        verbose=True,
    )

    start_time = time.perf_counter()
    next_sample_time = start_time

    while True:
        # Ждём точного момента выборки
        next_sample_time = sg.wait_for_sampling_period(
            sampling_frequency, next_sample_time
        )

        t = next_sample_time - start_time
        norm_amp = sg.get_triangle_wave_amplitude(signal_frequency, t)
        voltage = norm_amp * amplitude
        dac.set_voltage(voltage)

finally:
    dac.deinit()
