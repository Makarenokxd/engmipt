import numpy as np
import time


def get_sin_wave_amplitude(freq, moment):
    """
    Возвращает нормализованное значение синусоиды от 0 до 1.

    freq   - частота сигнала в Гц
    moment - момент времени в секундах
    """

    return (np.sin(2 * np.pi * freq * moment) + 1) / 2


def wait_for_sampling_period(sampling_frequency):
    """
    Ждёт один период дискретизации.
    """

    time.sleep(1 / sampling_frequency)