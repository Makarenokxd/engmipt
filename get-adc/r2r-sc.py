import r2r_adc as r2r
import adc_plot as plot
import time

dynamic_range = 3.183

adc = r2r.R2R_ADC(dynamic_range, compare_time=0.0001)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()

    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sc_voltage())
        time_values.append(time.time() - start_time)

    plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
