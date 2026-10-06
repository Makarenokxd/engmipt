import numpy as np
import time


def get_sin_wave_amplitude(freq, t):
    """
    Возвращает нормализованную амплитуду синусоиды в момент времени t.
    sin(2πft) ∈ [-1, 1] → сдвиг +1 → [0, 2] → деление /2 → [0, 1]
    """
    return (np.sin(2 * np.pi * freq * t) + 1) / 2


def wait_for_sampling_period(sampling_frequency, last_time):
    """
    Ждёт до наступления следующего периода дискретизации.
    Возвращает время следующей выборки для точного тайминга.
    """
    period = 1.0 / sampling_frequency
    next_time = last_time + period
    sleep_time = next_time - time.perf_counter()
    if sleep_time > 0:
        time.sleep(sleep_time)
    return next_time