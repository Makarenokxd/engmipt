import pwm_dac as pwm
import signal_generator as sg
import time

# ---------- параметры сигнала ----------
amplitude = 3.28           # В (чуть меньше dynamic_range = 3.290 В)
signal_frequency = 10      # Гц
sampling_frequency = 200   # Гц (20 точек на период; частота ШИМ 500 Гц)

# ---------- основная программа ----------
try:
    dac = pwm.PWM_DAC(
        gpio_pin=12,
        pwm_frequency=500,
        dynamic_range=3.290,
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
