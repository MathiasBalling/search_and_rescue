import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot


# ========================================================
# Load summary metadata for each test run
# ========================================================
summary_records = [
    ("test1.1", "1-moderate", "1-low", 1, 3),
    ("test1.2", "1-moderate", "1-low", 0, 1),
    ("test1.3", "1-moderate", "1-low", 1, 4),
    ("test1.4", "1-moderate", "1-low", 1, 1),
    ("test1.5", "1-moderate", "1-low", 1, 4),
    ("test1.6", "1-moderate", "1-low", 1, 3),
    ("test2.1", "1-moderate", "2-medium", 0, 2),
    ("test2.2", "1-moderate", "2-medium", 1, 1),
    ("test2.3", "1-moderate", "2-medium", 1, 2),
    ("test2.4", "1-moderate", "2-medium", 1, 3),
    ("test2.5", "1-moderate", "2-medium", 0, 2),
    ("test3.1", "1-moderate", "3-high", 1, 3),
    ("test3.2", "1-moderate", "3-high", 1, 1),
    ("test3.3", "1-moderate", "3-high", 1, 2),
    ("test4.1", "2-aggressive", "1-low", 1, 7),
    ("test4.2", "2-aggressive", "1-low", 0, 7),
    ("test4.3", "2-aggressive", "1-low", 1, 7),
    ("test5.1", "2-aggressive", "2-medium", 1, 7),
    ("test5.2", "2-aggressive", "2-medium", 1, 7),
    ("test5.3", "2-aggressive", "2-medium", 0, 7),
    ("test6.1", "2-aggressive", "3-high", 0, 2),
    ("test6.2", "2-aggressive", "3-high", 1, 4),
    ("test6.3", "2-aggressive", "3-high", 1, 6),
]

df = pd.DataFrame(
    summary_records, columns=["test_id", "speed", "pid", "success", "llr"]
)


# ========================================================
# Load raw sensor data and compute mean energy per second
# ========================================================
energy_values = {}

for file in glob.glob("./datalogs/*.csv"):
    test_name = os.path.splitext(os.path.basename(file))[0]
    raw = pd.read_csv(file)

    raw = raw.sort_values("time")

    # Compute power in Watts: P = V * I
    raw["power"] = (raw["voltage"] * 1e-6) * (raw["current"] * 1e-6)

    # Integrate energy via trapezoid rule (Joules)
    total_energy = np.trapezoid(raw["power"], raw["time"])

    # Compute duration
    duration = raw["time"].iloc[-1] - raw["time"].iloc[0]

    if duration > 0:
        avg_energy_per_second = total_energy / duration
    else:
        avg_energy_per_second = np.nan

    energy_values[test_name] = avg_energy_per_second

# Add to summary DataFrame
df["energy"] = df["test_id"].map(energy_values)

print("\n=== Summary with Avg Energy per second ===")
print(df)


# ========================================================
# Interaction plots
# ========================================================
# Keep ordered categorical in dataframe
# Ensure ordering

fig, ax = plt.subplots(figsize=(6, 4))
interaction_plot(df["pid"], df["speed"], df["llr"], ax=ax)
ax.set_title("Interaction plot – LLR")
plt.show()

fig, ax = plt.subplots(figsize=(6, 4))
interaction_plot(df["pid"], df["speed"], df["energy"], ax=ax)
ax.set_title("Interaction plot – Avg Energy per second")
plt.show()


# ========================================================
# Success rate
# ========================================================
print("\n=== Success rate ===")
# Calculate success rate for each speed and pid combination
success_rate = df.groupby(["speed", "pid"])["success"].mean().reset_index()

# Pivot for easier plotting
pivot = success_rate.pivot(index="pid", columns="speed", values="success")

# Plot
pivot.plot(kind="bar")
plt.ylabel("Success Rate")
plt.title("Success Rate by Speed and PID")
plt.xticks(rotation=0)
plt.legend(title="Speed")
plt.tight_layout()
plt.show()

# ========================================================
# Line loss recovery
# ========================================================
print("\n=== Line loss recovery ===")
# Calculate success rate for each speed and pid combination
success_rate = df.groupby(["speed", "pid"])["llr"].mean().reset_index()

# Pivot for easier plotting
pivot = success_rate.pivot(index="pid", columns="speed", values="llr")

# Plot
pivot.plot(kind="bar")
plt.ylabel("Line Loss Recovery")
plt.title("Line Loss Recovery by Speed and PID")
plt.xticks(rotation=0)
plt.legend(title="Speed")
plt.tight_layout()
plt.show()
