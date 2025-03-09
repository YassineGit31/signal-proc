import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import unit_impulse
from flask import Flask, render_template

app = Flask(__name__)

# Function to generate and save signal plots
def plot_and_save_signal(func, t_range, filename, title):
    t = np.linspace(t_range[0], t_range[1], 1000)
    y = func(t)

    plt.figure(figsize=(6, 4))
    plt.plot(t, y, label=title, color="b")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.legend()
    plt.title(title)
    plt.savefig(f"static/{filename}.png")
    plt.close()

# Define basic signals
def rect(t): return np.where(np.abs(t) <= 0.5, 1, 0)
def u(t): return np.where(t >= 0, 1, 0)
def tri(t): return np.where((t >= -1) & (t <= 1), 1 - np.abs(t), 0)
def delta(t): return unit_impulse(len(t), idx=len(t)//2)
def exp_signal(t): return np.exp(-t) * u(t)

# Define and generate signals based on the corrected formulas
plot_and_save_signal(lambda t: 2 * rect(2*t - 1), [-2, 2], "signal1", "x1(t) = 2Rect(2t-1)")
plot_and_save_signal(lambda t: np.sin(np.pi * t) * rect(t/2), [-2, 2], "signal2", "x2(t) = sin(πt) * Rect(t/2)")
plot_and_save_signal(lambda t: tri(t/2), [-2, 2], "signal3", "x3(t) = Tri(t/2)")
plot_and_save_signal(lambda t: u(t - 2), [-2, 4], "signal4", "x4(t) = U(t-2)")
plot_and_save_signal(lambda t: u(t - 3), [-2, 4], "signal5", "x5(t) = U(t-3)")
plot_and_save_signal(lambda t: 2 * delta(t+1) - delta(t-2) + delta(t) - 2 * delta(t-1), [-3, 3], "signal6", "x6(t) = 2δ(t+1) - δ(t-2) + δ(t) -2δ(t-1)")
plot_and_save_signal(lambda t: rect((t-1)/2) - rect((t+1)/2), [-3, 3], "signal7", "x7(t) = Rect((t-1)/2) - Rect((t+1)/2)")
plot_and_save_signal(lambda t: tri(t-1) - tri(t+1), [-3, 3], "signal8", "x8(t) = Tri(t-1) - Tri(t+1)")
plot_and_save_signal(lambda t: rect(t/2) - tri(t), [-3, 3], "signal9", "x9(t) = Rect(t/2) - Tri(t)")
plot_and_save_signal(lambda t: exp_signal(t-2), [-2, 4], "signal10", "x10(t) = exp(-t) * U(t-2)")
plot_and_save_signal(lambda t: np.sin(4 * np.pi * t), [-2, 2], "signal11", "x11(t) = sin(4πt)")

# Compute Average Power of x11(t)
T = 0.5  # Period of sin(4πt)
t = np.linspace(0, T, 1000)
x11 = np.sin(4 * np.pi * t)

P = (1 / T) * np.trapz(x11**2, t)  # Numerical integration

print(f"Puissance Moyenne (Average Power) of x11(t): {P:.4f}")  # Should be ~0.5


@app.route('/exercise1')
def exercise1():
    return render_template("exercise1.html")


if __name__ == '__main__':
    app.run(debug=True)
