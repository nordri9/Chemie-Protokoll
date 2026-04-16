import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Funktion zur Umrechnung von Wellenlänge in RGB-Farben


def wavelength_to_rgb(wavelength, gamma=0.8):
    """Konvertiert eine Wellenlänge in nm in einen RGB-Farbwert für den sichtbaren Bereich (380-750 nm)."""
    wl = float(wavelength)

    if 380 <= wl <= 440:
        attenuation = 0.3 + 0.7 * (wl - 380) / (440 - 380)
        R = (-(wl - 440) / (440 - 380)) * attenuation
        G = 0.0
        B = (1.0) * attenuation
    elif 440 < wl <= 490:
        R = 0.0
        G = (wl - 440) / (490 - 440)
        B = 1.0
    elif 490 < wl <= 510:
        R = 0.0
        G = 1.0
        B = -(wl - 510) / (510 - 490)
    elif 510 < wl <= 580:
        R = (wl - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif 580 < wl <= 645:
        R = 1.0
        G = -(wl - 645) / (645 - 580)
        B = 0.0
    elif 645 < wl <= 750:
        attenuation = 0.3 + 0.7 * (750 - wl) / (750 - 645)
        R = (1.0) * attenuation
        G = 0.0
        B = 0.0
    else:
        # Außerhalb des sichtbaren Spektrums (UV oder Infrarot) wird Schwarz verwendet
        R = 0.0
        G = 0.0
        B = 0.0

    # Gamma-Korrektur anwenden für realistischere Bildschirmdarstellung
    R = R ** gamma if R > 0 else 0
    G = G ** gamma if G > 0 else 0
    B = B ** gamma if B > 0 else 0

    return (R, G, B)


# Daten laden
data = np.loadtxt("CAROTIN9A-copy.txt", dtype=float, delimiter=",")
x = data[:, 0]
y = data[:, 1]

# Für jeden x-Wert (Wellenlänge) die exakte RGB-Farbe berechnen
colors = [wavelength_to_rgb(wl) for wl in x]

# Scatter-Plot mit der berechneten Farbliste erstellen
plt.scatter(x, y, c=colors, edgecolor='black',
            linewidth=0.2, label="Messwerte", zorder=5)

plt.title("Absorptionsspektrum")
plt.ylabel("Absorption")
plt.xlabel("Wellenlänge")

ax = plt.gca()

ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g} nm'))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g} A'))

plt.legend()
plt.savefig("../figures/fitten-von-funktionen.pdf")
plt.show()
