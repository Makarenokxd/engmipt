import mcp3021_driver as mcp
import adc_plot as plot
import time

dynamic_range = 5.11

adc = mcp.MCP3021(dynamic_range)

voltage_values = []
time_values = []
duration = 10.0

try:
    start_time = time.time()

    while time.time() - start_time < duration:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)

    plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
