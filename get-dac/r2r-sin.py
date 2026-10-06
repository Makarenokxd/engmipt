import r2r_dac as r2r
import signal_generator as sg
import time

# ---------- параметры сигнала ----------
amplitude = 3.2          # В (не больше dynamic_range ЦАП)
signal_frequency = 10    # Гц
sampling_frequency = 1000  # Гц

# ---------- основная программа ----------
try:
    dac = r2r.R2R_DAC(
        gpio_bits=[16, 20, 21, 25, 26, 17, 27, 22],
        dynamic_range=3.183,
        verbose=True,
    )

    start_time = time.time()

    while True:
        t = time.time() - start_time                       # время от начала
        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)  # 0 … 1
        voltage = norm_amp * amplitude                     # 0 … amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()