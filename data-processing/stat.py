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
# Print every line in the dataframe
for index, row in df.iterrows():
    print(row)

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
stats.probplot(df["total_energy"].dropna(), dist="norm", plot=plt)
plt.title("QQ-plot of Energy")
plt.tight_layout()
plt.show()

# TODO: Change to bartlett
# Levene's test for homogeneity of variances (LLR by p_gain)
levene_llr = stats.levene(
    *[group["llr"].values for name, group in df.groupby("p_gain")]
)
print(
    f"Levene's test for LLR by p_gain: stat={levene_llr.statistic:.3f}, p={levene_llr.pvalue:.3g}"
)

# Levene's test for Energy by p_gain
levene_energy = stats.levene(
    *[group["total_energy"].dropna().values for name, group in df.groupby("p_gain")]
)
print(
    f"Levene's test for Energy by p_gain: stat={levene_energy.statistic:.3f}, p={levene_energy.pvalue:.3g}"
)

bartlett_llr = stats.bartlett(
    *[group["llr"].values for _, group in df.groupby("p_gain")]
)
print(
    f"Bartlett's test for LLR by p_gain: stat={bartlett_llr.statistic:.3f}, p={bartlett_llr.pvalue:.3g}"
)

# Bartlett's test for Energy by p_gain
bartlett_energy = stats.bartlett(
    *[group["total_energy"].dropna().values for _, group in df.groupby("p_gain")]
)
print(
    f"Bartlett's test for Energy by p_gain: stat={bartlett_energy.statistic:.3f}, p={bartlett_energy.pvalue:.3g}"
)

# ========================================================
# Two-way ANOVA – LLR
# ========================================================
print("\n=== ANOVA LLR ===")
model_llr = smf.ols("llr ~ C(speed_mode) * C(p_gain)", data=df).fit()
print(anova_lm(model_llr, typ=2))

# ========================================================
# Two-way ANOVA – Avg Energy
# ========================================================
print("\n=== ANOVA Energy (Avg per second) ===")
model_energy = smf.ols("total_energy ~ C(speed_mode) * C(p_gain)", data=df).fit()
print(anova_lm(model_energy, typ=2))

# ========================================================
# Tukey HSD – groups
# ========================================================
print("\n=== Tukey test for LLR (P) ===")
print(pairwise_tukeyhsd(df["llr"], df["p_gain"]))

print("\n=== Tukey test for Energy (P) ===")
print(pairwise_tukeyhsd(df["total_energy"], df["p_gain"]))

# ========================================================
# Tukey HSD – groups
# ========================================================
print("\n=== Tukey test for LLR (speed_mode) ===")
print(pairwise_tukeyhsd(df["llr"], df["speed_mode"]))

print("\n=== Tukey test for Energy (speed_mode) ===")
print(pairwise_tukeyhsd(df["total_energy"], df["speed_mode"]))


# # ========================================================
# # Plot Energy vs LLR correlation
# # ========================================================
# plt.figure(figsize=(8, 6))
# plt.scatter(
#     df["total_energy"], df["llr"], color="blue", s=80, alpha=0.7, label="Test points"
# )
#
# # Fit a linear regression line for visualization
# slope, intercept = np.polyfit(df["total_energy"], df["llr"], 1)
# plt.plot(
#     df["total_energy"],
#     slope * df["total_energy"] + intercept,
#     color="red",
#     label=f"Fit: y={slope:.2f}x+{intercept:.2f}",
# )
#
# plt.xlabel("Average Energy per second (J/s)")
# plt.ylabel("LLR")
# plt.title("Correlation between total_energy and LLR")
# plt.grid(True, linestyle="--", alpha=0.5)
# plt.legend()
# plt.tight_layout()
# plt.show()
#
# # Compute correlation coefficient
# corr = df["total_energy"].corr(df["llr"])
# print(f"Pearson correlation coefficient between total_energy and LLR: {corr:.3f}")
