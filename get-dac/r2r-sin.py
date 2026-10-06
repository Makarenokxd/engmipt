import r2r_dac as r2r
import signal_generator as sg
import time


# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


try:
    # Создаём объект ЦАП
    dac = r2r.R2R_DAC()

    # Время начала генерации
    start_time = time.perf_counter()

    # Номер текущей точки
    sample_number = 0

    while True:

        # Момент времени, для которого рассчитываем сигнал
        current_time = time.perf_counter() - start_time

        # Рассчитываем нормализованную синусоиду
        normalized_value = sg.get_sin_wave_amplitude(
            signal_frequency,
            current_time
        )

        # Переводим её в напряжение
        voltage = normalized_value * amplitude

        # Выводим напряжение через R2R ЦАП
        dac.set_voltage(voltage)

        # Следующая точка должна появиться
        # ровно через один период дискретизации
        sample_number += 1

        next_sample_time = (
            start_time
            + sample_number / sampling_frequency
        )

        # Ждём до момента следующей точки
        while time.perf_counter() < next_sample_time:
            pass


finally:
    # Выключаем/освобождаем ЦАП
    dac.deinit()