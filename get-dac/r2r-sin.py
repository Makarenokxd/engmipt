import r2r_dac as r2r
import signal_generator as sg
import time

# ---------- параметры сигнала ----------
amplitude = 1           # В (чуть меньше dynamic_range = 3.183 В)
signal_frequency = 1      # Гц
sampling_frequency = 5  # Гц (200 точек на период для гладкости)

# ---------- основная программа ----------
try:
    dac = r2r.R2R_DAC(
        gpio_bits=[22, 27, 17, 26, 25, 21, 20, 16],
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
        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = norm_amp * amplitude
        dac.set_voltage(voltage)

finally:
    dac.deinit()