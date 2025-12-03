import matplotlib.pyplot as plt
from load import load_data
import seaborn as sns


plt.rcParams.update({"font.size": 14})
# ========================================================
# Load and process data from folders
# ========================================================
df = load_data()

# Averaage lenght of the run
print("\n=== Average length of the run ===")
print(df["completion_time"].mean())

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

print("\n=== Line loss recovery ===")
# Box plot for LLR by speed and p_gain

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="p_gain", y="llr", hue="speed_mode")
plt.ylabel("Line Loss Recovery", fontsize=16)
plt.xlabel("p_gain", fontsize=16)
plt.title("Line Loss Recovery by Speed and PID", fontsize=18)
plt.legend(title="Speed", fontsize=14, title_fontsize=15)
plt.tight_layout()
plt.show()

print("\n=== Avg Energy per run ===")
# Box plot for total_energy by speed and p_gain
plt.figure(figsize=(8, 6))
sns.boxplot(
    data=df,
    x="p_gain",
    y="total_energy",
    hue="speed_mode",
)
plt.ylabel("Energy per run", fontsize=16)
plt.title("Energy per run by Speed and PID", fontsize=18)
plt.xlabel("p_gain", fontsize=16)
plt.legend(title="Speed", fontsize=14, title_fontsize=15)
plt.tight_layout()
plt.show()

print("\n=== Completion Time ===")
plt.figure(figsize=(8, 6))
sns.boxplot(
    data=df,
    x="p_gain",
    y="completion_time",
    hue="speed_mode",
)
plt.ylabel("Completion Time", fontsize=16)
plt.title("Completion Time by Speed and PID", fontsize=18)
plt.xlabel("p_gain", fontsize=16)
plt.legend(title="Speed", fontsize=14, title_fontsize=15)
plt.tight_layout()
plt.show()
