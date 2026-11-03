# График U(t) по файлу rc_data.csv и оценка постоянной времени tau = R*C.
import sys
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "rc_data.csv"
data = np.loadtxt(FILE_NAME, delimiter=",", skiprows=1)
t, u = data[:, 0], data[:, 1]

# tau по первой зарядке: время роста от минимума до 63% от размаха
u_min, u_max = u.min(), u.max()
i0 = np.argmax(u < u_min + 0.05 * (u_max - u_min))
level = u_min + 0.63 * (u_max - u_min)
rise = np.where((np.arange(len(u)) > i0) & (u >= level))[0]
title = "Зарядка и разрядка конденсатора"
if len(rise):
    start = np.where(u[:rise[0]] <= u_min + 0.05 * (u_max - u_min))[0][-1]
    tau = t[rise[0]] - t[start]
    title += f"  (tau ≈ {tau * 1000:.0f} мс)"

plt.plot(t, u, ".-", markersize=2)
plt.title(title)
plt.xlabel("Время, с")
plt.ylabel("Напряжение на C1, В")
plt.grid(True)
plt.savefig("rc_plot.png", dpi=150)
plt.show()
