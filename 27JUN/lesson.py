import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(0, 4 * np.pi, 1000)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_title('正弦與餘弦波形')
ax.set_xlabel('x')
ax.set_ylabel('y')

sin_line, = ax.plot(x, np.sin(x), label='sin(x)', color='#1f77b4', linewidth=2)
cos_line, = ax.plot(x, np.cos(x), label='cos(x)', color='#ff7f0e', linewidth=2)
ax.legend(loc='upper right')

ax_slider_amp = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_slider_freq = plt.axes([0.15, 0.07, 0.7, 0.03])
ax_slider_phase = plt.axes([0.15, 0.02, 0.7, 0.03])

slider_amp = Slider(ax_slider_amp, '振幅 A', 0.1, 5.0, valinit=1.0, valstep=0.05)
slider_freq = Slider(ax_slider_freq, '頻率 ω', 0.1, 10.0, valinit=1.0, valstep=0.05)
slider_phase = Slider(ax_slider_phase, '相位 φ (rad)', 0, 2 * np.pi, valinit=0.0, valstep=0.01)

def update(val):
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    sin_line.set_ydata(A * np.sin(omega * x + phi))
    cos_line.set_ydata(A * np.cos(omega * x + phi))

    ax.set_ylim(-A * 1.5, A * 1.5)
    fig.canvas.draw_idle()

slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()
