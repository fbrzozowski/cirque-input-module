import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons


def sigmoid(delta, threshold, factor):
    return delta * (1.0 / (1.0 + np.exp(-factor * (np.abs(delta) / threshold - 1.0))))


def hybrid(delta, threshold, exponent, factor):
    return np.sign(delta) * np.tanh(np.power(np.abs(delta) / threshold, exponent)) * threshold * factor


deltas = np.linspace(-127, 128, 5000)
color_options = [
    '#ffffff', '#00ffff', '#ff00ff', '#ffff00', '#00ff00',
    '#ff9900', '#9999ff', '#66ffcc', '#ff6666', '#cccccc',
]

init_color = color_options[0]
init_threshold = 50
init_factor = 2.0
init_exponent = 1.5
init_width = 1.5
init_style = 'solid'

plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(14, 10))
plt.subplots_adjust(left=0.28, bottom=0.05, right=0.98, top=0.97)
fig.patch.set_facecolor('#383838')
ax.set_facecolor("#2b2b2b")
ax.set_xlim(-128, 128)
ax.set_ylim(-128, 128)
ax.set_xlabel("Input Delta", color="#c9c9c9")
ax.set_ylabel("Accelerated Output", color="#c9c9c9")
ax.grid(True, color="#383838")

curves = []
current_color = [init_color]

x0 = 0.03
width = 0.22
h = 0.03
pad = 0.005
start = 0.90

s_threshold = Slider(plt.axes([x0, start - 0 * h - 0 * pad, width, h]), 'Threshold', 1, 128, valinit=init_threshold)
s_factor = Slider(plt.axes([x0, start - 1 * h - 1 * pad, width, h]), 'Factor', 0.1, 5.0, valinit=init_factor)
s_exponent = Slider(plt.axes([x0, start - 2 * h - 2 * pad, width, h]), 'Exponent', 0.1, 5.0, valinit=init_exponent)
s_width = Slider(plt.axes([x0, start - 3 * h - 3 * pad, width, h]), 'Line Width', 0.5, 5.0, valinit=init_width)

radio_type = RadioButtons(plt.axes([x0, 0.65, width, 0.08]), ('hybrid', 'sigmoid'))
radio_style = RadioButtons(plt.axes([x0, 0.53, width, 0.12]), ('solid', 'dashed', 'dashdot', 'dotted'))

radio_color = RadioButtons(
    plt.axes([x0, 0.25, width, 0.25]),
    color_options,
    label_props={'color': color_options},
    radio_props={'s': [20] * len(color_options)}
)

b_add = Button(plt.axes([x0, 0.13, width, 0.04]), 'Add Curve')
b_clear = Button(plt.axes([x0, 0.07, width, 0.04]), 'Clear All')

preview_line, = ax.plot(
    deltas,
    hybrid(deltas, init_threshold, init_exponent, init_factor),
    label="preview",
    color=init_color,
    linewidth=init_width,
    linestyle=init_style
)


def update_preview(val=None):
    t = s_threshold.val
    f = s_factor.val
    e = s_exponent.val
    w = s_width.val
    style = radio_style.value_selected
    mode = radio_type.value_selected

    y = hybrid(deltas, t, e, f) if mode == 'hybrid' else sigmoid(deltas, t, f)

    preview_line.set_ydata(y)
    preview_line.set_color(current_color[0])
    preview_line.set_linestyle(style)
    preview_line.set_linewidth(w)
    fig.canvas.draw_idle()


def on_color_change(label):
    current_color[0] = label
    update_preview()


s_threshold.on_changed(update_preview)
s_factor.on_changed(update_preview)
s_exponent.on_changed(update_preview)
s_width.on_changed(update_preview)
radio_type.on_clicked(update_preview)
radio_style.on_clicked(update_preview)
radio_color.on_clicked(on_color_change)


def add_curve(event):
    t = s_threshold.val
    f = s_factor.val
    e = s_exponent.val
    w = s_width.val
    style = radio_style.value_selected
    mode = radio_type.value_selected

    y = hybrid(deltas, t, e, f) if mode == 'hybrid' else sigmoid(deltas, t, f)
    label = f"{mode} T={t:.1f}, E={e:.1f}, F={f:.1f}" if mode == 'hybrid' else f"{mode} T={t:.1f}, F={f:.1f}"

    line, = ax.plot(deltas, y, label=label, color=current_color[0], linestyle=style, linewidth=w)
    curves.append(line)
    ax.legend()
    fig.canvas.draw_idle()


def clear_all(event):
    for line in curves:
        line.remove()
    curves.clear()
    ax.legend()
    fig.canvas.draw_idle()


b_add.on_clicked(add_curve)
b_clear.on_clicked(clear_all)

update_preview()
plt.show()
