import pandas as pd
import scipy.stats as stats
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.factorplots import interaction_plot
import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.factorplots import interaction_plot


# ========================================================
# Load summary metadata for each test run
# ========================================================
summary_records = [
    ("test1.1", "moderate", "low", 1, 3),
    ("test1.2", "moderate", "low", 0, 1),
    ("test1.3", "moderate", "low", 1, 4),
    ("test1.4", "moderate", "low", 1, 1),
    ("test1.5", "moderate", "low", 1, 4),
    ("test1.6", "moderate", "low", 1, 3),
    ("test2.1", "moderate", "medium", 0, 2),
    ("test2.2", "moderate", "medium", 1, 1),
    ("test2.3", "moderate", "medium", 1, 2),
    ("test2.4", "moderate", "medium", 1, 3),
    ("test2.5", "moderate", "medium", 0, 2),
    ("test3.1", "moderate", "high", 1, 3),
    ("test3.2", "moderate", "high", 1, 1),
    ("test3.3", "moderate", "high", 1, 2),
    ("test4.1", "aggressive", "low", 1, 7),
    ("test4.2", "aggressive", "low", 0, 7),
    ("test4.3", "aggressive", "low", 1, 7),
    ("test5.1", "aggressive", "medium", 1, 7),
    ("test5.2", "aggressive", "medium", 1, 7),
    ("test5.3", "aggressive", "medium", 0, 7),
    ("test6.1", "aggressive", "high", 0, 2),
    ("test6.2", "aggressive", "high", 1, 4),
    ("test6.3", "aggressive", "high", 1, 6),
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
# QQ-plot and Levene's test for normality and homogeneity
# ========================================================

# QQ-plot for LLR
plt.figure(figsize=(6, 6))
stats.probplot(df["llr"], dist="norm", plot=plt)
plt.title("QQ-plot of LLR")
plt.tight_layout()
plt.show()

# QQ-plot for Energy
plt.figure(figsize=(6, 6))
stats.probplot(df["energy"].dropna(), dist="norm", plot=plt)
plt.title("QQ-plot of Energy")
plt.tight_layout()
plt.show()

# TODO: Change to bartlett
# Levene's test for homogeneity of variances (LLR by pid)
levene_llr = stats.levene(*[group["llr"].values for name, group in df.groupby("pid")])
print(
    f"Levene's test for LLR by pid: stat={levene_llr.statistic:.3f}, p={levene_llr.pvalue:.3g}"
)

# Levene's test for Energy by pid
levene_energy = stats.levene(
    *[group["energy"].dropna().values for name, group in df.groupby("pid")]
)
print(
    f"Levene's test for Energy by pid: stat={levene_energy.statistic:.3f}, p={levene_energy.pvalue:.3g}"
)

# ========================================================
# Two-way ANOVA – LLR
# ========================================================
print("\n=== ANOVA LLR ===")
model_llr = smf.ols("llr ~ C(speed) * C(pid)", data=df).fit()
print(anova_lm(model_llr, typ=2))

# ========================================================
# Two-way ANOVA – Avg Energy
# ========================================================
print("\n=== ANOVA Energy (Avg per second) ===")
model_energy = smf.ols("energy ~ C(speed) * C(pid)", data=df).fit()
print(anova_lm(model_energy, typ=2))

# ========================================================
# Tukey HSD – groups
# ========================================================
print("\n=== Tukey test for LLR (P) ===")
print(pairwise_tukeyhsd(df["llr"], df["pid"]))

print("\n=== Tukey test for Energy (P) ===")
print(pairwise_tukeyhsd(df["energy"], df["pid"]))

# ========================================================
# Tukey HSD – groups
# ========================================================
print("\n=== Tukey test for LLR (speed) ===")
print(pairwise_tukeyhsd(df["llr"], df["speed"]))

print("\n=== Tukey test for Energy (speed) ===")
print(pairwise_tukeyhsd(df["energy"], df["speed"]))

# ========================================================
# Logistic regression
# ========================================================
print("\n=== Logistic regression ===")
logit_model = smf.logit("success ~ C(speed) * C(pid)", data=df).fit()
print(logit_model.summary())

# ========================================================
# Plot Energy vs LLR correlation
# ========================================================
plt.figure(figsize=(8, 6))
plt.scatter(df["energy"], df["llr"], color="blue", s=80, alpha=0.7, label="Test points")

# Fit a linear regression line for visualization
slope, intercept = np.polyfit(df["energy"], df["llr"], 1)
plt.plot(
    df["energy"],
    slope * df["energy"] + intercept,
    color="red",
    label=f"Fit: y={slope:.2f}x+{intercept:.2f}",
)

plt.xlabel("Average Energy per second (J/s)")
plt.ylabel("LLR")
plt.title("Correlation between Energy and LLR")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# Compute correlation coefficient
corr = df["energy"].corr(df["llr"])
print(f"Pearson correlation coefficient between energy and LLR: {corr:.3f}")
