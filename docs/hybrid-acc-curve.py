# Re-import required libraries after code execution state reset
import matplotlib.pyplot as plt
import numpy as np


# Sigmoid acceleration function
def sigmoid(delta, threshold, factor):
    return delta * (1.0 / (1.0 + np.exp(-factor * (np.abs(delta) / threshold - 1.0))))


# Polynomial acceleration function
def polynomial(delta, threshold, exponent):
    return np.sign(delta) * np.power(np.abs(delta) / threshold, exponent) * threshold


# Hybrid (tanh of polynomial)
def hybrid(delta, threshold, exponent, factor):
    norm = np.abs(delta) / threshold
    poly = np.power(norm, exponent)
    tanh_curve = np.tanh(poly)
    return np.sign(delta) * tanh_curve * threshold * factor


# Input range
deltas = np.linspace(-20, 20, 400)

# Parameter sets
configs = [

    # {"title": "Low factor/threshold: 5/1.25/2 (ths/exp/f)", "thr": 5, "exp": 1.25, "f": 2},
    # {"title": "High expo: 10/2.75/2 (ths/exp/f)", "thr": 10, "exp": 2.75, "f": 2},
    # {"title": "High expo/treshold: 15/2.75/2 (ths/exp/f)", "thr": 15, "exp": 2.75, "f": 2},
    #
    # {"title": "Low threshold: 5/2/2 (ths/exp/f)", "thr": 5, "exp": 2, "f": 2},
    # {"title": "Base: 10/2/2 (ths/f/exp)", "thr": 10, "exp": 2, "f": 2},
    # {"title": "High threshold: 15/2/2 (ths/exp/f)", "thr": 15, "exp": 2, "f": 2},
    #
    #
    # {"title": "Low expo/threshold: 5/1.25/2 (ths/exp/f)", "thr": 10, "exp": 2, "f": 2},
    # {"title": "Low expo: 10/1.25/2 (ths/exp/f)", "thr": 10, "exp": 2, "f": 2},
    # {"title": "High Threshold / Low expo: 15/2/3 (ths/exp/f)", "thr": 15, "exp": 2, "f": 2},

    {"title": "Low threshold/High factor: 5/2.75/2 (ths/f/exp)", "thr": 5, "f": 2.75, "exp": 2},
    {"title": "High factor: 10/2.75/2 (ths/f/exp)", "thr": 10, "f": 2.75, "exp": 2},
    {"title": "High threshold/factor: 15/2.75/2 (ths/f/exp)", "thr": 15, "f": 2.75, "exp": 2},

    {"title": "Low threshold: 5/2/2 (ths/f/exp)", "thr": 5, "f": 2, "exp": 2},
    {"title": "Base: 10/2/2 (ths/f/exp)", "thr": 10, "f": 2, "exp": 2},
    {"title": "High threshold: 15/2/2 (ths/f/exp)", "thr": 15, "f": 2, "exp": 2},

    {"title": "Low factor/threshold: 5/1.25/2 (ths/f/exp)", "thr": 5, "f": 1.25, "exp": 2},
    {"title": "Low factor: 10/1.25/2 (ths/f/exp)", "thr": 10, "f": 1.25, "exp": 2},
    {"title": "Low factor/High treshold: 15/1.25/2 (ths/f/exp)", "thr": 15, "f": 1.25, "exp": 2},
]

# Plotting
plt.style.use("dark_background")
fig, axs = plt.subplots(3, 3, figsize=(14, 10))
axs = axs.flatten()
fig.patch.set_facecolor('#383838')

for i, cfg in enumerate(configs):
    s = sigmoid(deltas, cfg["thr"], cfg["f"])
    p = polynomial(deltas, cfg["thr"], cfg["exp"])
    h = hybrid(deltas, cfg["thr"], cfg["exp"], cfg["f"])

    axs[i].plot(deltas, s, label="Sigmoid", linestyle="--")
    axs[i].plot(deltas, p, label="Polynomial", linestyle="-.", color="magenta")
    axs[i].plot(deltas, h, label="Hybrid (Tanh of Poly)", linewidth=2, color="orange")
    axs[i].set_title(cfg["title"], color="#c9c9c9")
    axs[i].set_xlabel("Input Delta", color="#c9c9c9")
    axs[i].set_ylabel("Accelerated Output", color="#c9c9c9")
    axs[i].set_facecolor("#2b2b2b")  # Dark gray axes background
    axs[i].grid(True, color="#383838")
    axs[i].legend()

plt.tight_layout()
plt.show()
