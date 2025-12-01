import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.oneway import anova_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from load import load_data

# ========================================================
# Load and process data from folders
# ========================================================
df = load_data()

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

# Levene's test for homogeneity of variances (LLR by speed_mode)
levene_llr = stats.levene(
    *[group["llr"].values for name, group in df.groupby("speed_mode")]
)
print(
    f"Levene's test for LLR by speed_mode: stat={levene_llr.statistic:.3f}, p={levene_llr.pvalue:.3g}"
)
# Levene's test for Energy by speed_mode
levene_energy = stats.levene(
    *[group["total_energy"].dropna().values for name, group in df.groupby("speed_mode")]
)
print(
    f"Levene's test for Energy by speed_mode: stat={levene_energy.statistic:.3f}, p={levene_energy.pvalue:.3g}"
)

bartlett_llr = stats.bartlett(
    *[group["llr"].values for _, group in df.groupby("speed_mode")]
)
print(
    f"Bartlett's test for LLR by speed_mode: stat={bartlett_llr.statistic:.3f}, p={bartlett_llr.pvalue:.3g}"
)

# Bartlett's test for Energy by speed_mode
bartlett_energy = stats.bartlett(
    *[group["total_energy"].dropna().values for _, group in df.groupby("speed_mode")]
)
print(
    f"Bartlett's test for Energy by speed_mode: stat={bartlett_energy.statistic:.3f}, p={bartlett_energy.pvalue:.3g}"
)

# ========================================================
# Two-way ANOVA – LLR
# ========================================================
print("\n=== ANOVA LLR ===")
model_llr = smf.ols("llr ~ C(speed_mode) * C(p_gain)", data=df).fit()
print(anova_lm(model_llr, typ=2))

print("\n=== ANOVA Energy (Avg per second) ===")
model_energy = smf.ols("total_energy ~ C(speed_mode) * C(p_gain)", data=df).fit()
print(anova_lm(model_energy, typ=2))

# ========================================================
# One-way ANOVA
# ========================================================
print("\n=== Welch's ANOVA for LLR by p_gain ===")
welch_llr_pgain = anova_oneway(
    [group["llr"].values for _, group in df.groupby("p_gain")], use_var="unequal"
)
print(welch_llr_pgain)

print("\n=== Welch's ANOVA for Energy by p_gain ===")
welch_energy_pgain = anova_oneway(
    [group["total_energy"].dropna().values for _, group in df.groupby("p_gain")],
    use_var="unequal",
)
print(welch_energy_pgain)

print("\n=== Welch's ANOVA for LLR by speed_mode ===")
welch_llr_speed = anova_oneway(
    [group["llr"].values for _, group in df.groupby("speed_mode")], use_var="unequal"
)
print(welch_llr_speed)

print("\n=== Welch's ANOVA for Energy by speed_mode ===")
welch_energy_speed = anova_oneway(
    [group["total_energy"].dropna().values for _, group in df.groupby("speed_mode")],
    use_var="unequal",
)
print(welch_energy_speed)
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
