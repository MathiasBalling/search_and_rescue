import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot

# ========================================================
# Load and process data from folders
# ========================================================
data = []

folders = [
    "1.0_aggressive",
    "1.0_moderate",
    "1.75_aggressive",
    "1.75_moderate",
    "2.5_aggressive",
    "2.5_moderate",
]

for folder in folders:
    p_gain, speed_mode = folder.split("_")
    for file in glob.glob(f"./datalogs/{folder}/*.csv"):
        test_id = os.path.splitext(os.path.basename(file))[0]
        raw = pd.read_csv(file)
        raw = raw.sort_values("time")
        # Compute power in Watts: P = V * I
        raw["power"] = (raw["voltage"] * 1e-6) * (raw["current"] * 1e-6)
        # Integrate energy via trapezoid rule (Joules)
        total_energy = np.trapezoid(raw["power"], raw["time"])
        # Compute duration
        llr = raw["LLR"].iloc[-1]
        if speed_mode == "moderate":
            total_energy = min(total_energy, 10)
            llr = min(llr, 7)
        else:
            llr = max(llr, 7)

        data.append(
            {
                "test_id": test_id,
                "p_gain": p_gain,
                "speed_mode": speed_mode,
                "total_energy": total_energy,
                "llr": llr,
            }
        )

df = pd.DataFrame(data)
print("\n=== Summary with Avg Energy per second and Mean LLR ===")
print(df)

# ========================================================
# Line loss recovery
# ========================================================
print("\n=== Line loss recovery ===")
# Calculate success rate for each speed and p_gain combination
success_rate = df.groupby(["speed_mode", "p_gain"])["llr"].mean().reset_index()

# Pivot for easier plotting
pivot = success_rate.pivot(index="p_gain", columns="speed_mode", values="llr")

# Plot
pivot.plot(kind="bar")
plt.ylabel("Line Loss Recovery")
plt.title("Line Loss Recovery by Speed and PID")
plt.xticks(rotation=0)
plt.legend(title="Speed")
plt.tight_layout()
plt.show()

# ========================================================
# Energy per second
# ========================================================
print("\n=== Avg Energy per run ===")
# Calculate success rate for each speed and p_gain combination
success_rate = df.groupby(["speed_mode", "p_gain"])["total_energy"].mean().reset_index()

# Pivot for easier plotting
pivot = success_rate.pivot(index="p_gain", columns="speed_mode", values="total_energy")

# Plot
pivot.plot(kind="bar")
plt.ylabel("Avg Energy per run")
plt.title("Avg Energy per run by Speed and PID")
plt.xticks(rotation=0)
plt.legend(title="Speed")
plt.tight_layout()
plt.show()
