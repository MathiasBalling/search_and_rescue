import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Raw data: base_speed, success, run_time
data = [
    (0.125, 0, 0),
    (0.125, 1, 158.06),
    (0.125, 0, 0),
    (0.125, 1, 157.16),
    (0.125, 0, 0),
    (0.125, 0, 0),
    (0.125, 1, 155.47),
    (0.125, 1, 147.58),
    (0.125, 0, 0),
    (0.125, 0, 0),
    (0.2, 0, 0),
    (0.2, 1, 112.4),
    (0.2, 1, 115.24),
    (0.2, 0, 0),
    (0.2, 1, 119.64),
    (0.2, 1, 107.07),
    (0.2, 0, 0),
    (0.2, 1, 108.34),
    (0.2, 1, 108.07),
    (0.2, 1, 115.15),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 0, 0),
    (0.275, 1, 107),
]

# Create DataFrame
df = pd.DataFrame(data, columns=["base_speed", "success", "run_time"])

# Keep only successful runs
time_df = df[df["success"] == 1]

# Plot
plt.figure(figsize=(8, 6))
sns.boxplot(
    data=time_df,
    x="base_speed",
    y="run_time",
)

plt.ylabel("Completion Time (s)", fontsize=16)
plt.xlabel("Base Speed (m/s)", fontsize=16)
plt.title("Completion Time for Successful Runs by Base Speed", fontsize=18)
plt.tight_layout()
plt.savefig("base_speed_time.png")
plt.show()

success_rate = (
    df[df["success"] == 1].groupby("base_speed").size()
    / pd.DataFrame(data, columns=["base_speed", "success", "run_time"])
    .groupby("base_speed")
    .size()
)
plt.figure(figsize=(8, 6))
sns.barplot(x=success_rate.index, y=success_rate.values)
plt.ylabel("Success Rate", fontsize=16)
plt.xlabel("Base Speed (m/s)", fontsize=16)
plt.title("Success Rate by Base Speed", fontsize=18)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("base_speed_success.png")
plt.show()
