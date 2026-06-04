import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Parameter
# -----------------------------
c_acid = 0.0448          # mol/L (verdünnte Essigsäure)
V_acid = 0.025           # L
Ka = 1.8e-5
pKa = -np.log10(Ka)
c_base = 0.1             # mol/L

n_acid = c_acid * V_acid
V_eq = n_acid / c_base   # Äquivalenzpunkt
V_half = V_eq / 2        # Halbäquivalenzpunkt

Kw = 1e-14
V_base_added = np.linspace(0, 0.022, 500)  # bis 22 mL NaOH
pH_values = []

# -----------------------------
# Titrationskurve berechnen
# -----------------------------
for Vb in V_base_added:
    n_base = c_base * Vb
    V_total = V_acid + Vb

    if n_base < n_acid:  # vor Äquivalenzpunkt
        n_HAc = n_acid - n_base
        n_Ac = n_base
        pH = pKa + np.log10(n_Ac / n_HAc) if n_Ac > 0 else - \
            np.log10(np.sqrt(Ka * c_acid))
    elif np.isclose(n_base, n_acid, atol=1e-8):  # Äquivalenzpunkt
        c_acetate = n_acid / V_total
        Kb = Kw / Ka
        OH = np.sqrt(Kb * c_acetate)
        pOH = -np.log10(OH)
        pH = 14 - pOH
    else:  # Überschuss OH-
        n_excess = n_base - n_acid
        OH = n_excess / V_total
        pOH = -np.log10(OH)
        pH = 14 - pOH

    pH_values.append(pH)
    
# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10, 6))
plt.plot(V_base_added * 1000, pH_values, color="darkblue",
         linewidth=2, label="Titrationskurve")

# Halbäquivalenzpunkt markieren
plt.scatter(V_half*1000, pKa, color="orange", zorder=5,
            label=f"Halbäquivalenzpunkt pH≈{pKa:.2f}")
plt.axvline(V_half*1000, color="orange", linestyle="--")

# Äquivalenzpunkt markieren
plt.scatter(V_eq*1000, 8.62, color="red", zorder=5,
            label=f"Äquivalenzpunkt pH≈8.62")
plt.axvline(V_eq*1000, color="red", linestyle="--")

# Achsen & Titel
plt.xlabel("zugegebenes Volumen 0,1 mol/L NaOH [mL]", fontsize=16)
plt.ylabel("pH-Wert", fontsize=16)
plt.grid(False)
plt.legend()
plt.ylim(0, 14)
plt.xlim(0, 22)

# pH-Achse in 1er-Schritten beschriften
plt.yticks(np.arange(0, 15, 1))

# Gitternetzlinien entfernen
# plt.grid(True)

# Legende anzeigen
plt.legend()

# Layout optimieren
plt.tight_layout()

# Grafik als PDF speichern
plt.savefig("python/titrationskurve.pdf")

# Grafik schließen, gut für Skripte
plt.close()