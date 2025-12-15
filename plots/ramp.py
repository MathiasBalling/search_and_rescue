import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Raw data: Wheel condition, Success
data = [
    ("Dirty wheels", 0),
    ("Dirty wheels", 0),
    ("Dirty wheels", 0),
    ("Dirty wheels", 0),
    ("Dirty wheels", 0),
    ("Dirty wheels", 1),
    ("Dirty wheels", 0),
    ("Dirty wheels", 0),
    ("Dirty wheels", 1),
    ("Dirty wheels", 0),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Clean wheels", 0),
    ("Clean wheels", 0),
    ("Clean wheels", 1),
    ("Clean wheels", 1),
    ("Rubber bands", 1),
    ("Rubber bands", 1),
    ("Rubber bands", 1),
    ("Rubber bands", 1),
    ("Rubber bands", 0),
    ("Rubber bands", 0),
    ("Rubber bands", 1),
    ("Rubber bands", 0),
    ("Rubber bands", 1),
    ("Rubber bands", 0),
]

# Create DataFrame
df = pd.DataFrame(data, columns=["Wheel condition", "Success"])

# Calculate success rate by wheel condition
success_rate = (
    df[df["Success"] == 1].groupby("Wheel condition").size()
    / df.groupby("Wheel condition").size()
)

plt.figure(figsize=(8, 6))
sns.barplot(
    x=success_rate.index,
    y=success_rate.values,
    order=["Dirty wheels", "Clean wheels", "Rubber bands"],
)
plt.ylabel("Success Rate", fontsize=16)
plt.xlabel("Wheel Condition", fontsize=16)
plt.title("Success Rate by Wheel Condition", fontsize=18)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("wheel_condition_success.png")
plt.show()
