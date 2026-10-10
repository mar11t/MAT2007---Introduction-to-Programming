import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Setup paths
DATA_PATH = "data/incidence-of-tuberculosis-sdgs.csv"
FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# 2. Load dataset
df = pd.read_csv(DATA_PATH)

# Identify the rate column dynamically
rate_col = [col for col in df.columns if col not in ['Entity', 'Code', 'Year']][0]

# Filter out regional aggregates (retaining sovereign entities with 3-letter ISO codes)
cdf = df[df['Code'].notna() & (df['Code'].str.len() == 3)].copy()

# ==========================================
# FIGURE 1: Top 5 Countries in 2024
# ==========================================
target_year = 2024 if 2024 in cdf['Year'].values else cdf['Year'].max()
df_latest = cdf[cdf['Year'] == target_year].sort_values(by=rate_col, ascending=False)
top_5 = df_latest.head(5).copy()

# Poisson counting uncertainty per 100,000 population: sigma = sqrt(Rate)
top_5['uncertainty'] = np.sqrt(top_5[rate_col])

fig, ax = plt.subplots(figsize=(6.8, 4.0))
bars = ax.barh(top_5['Entity'][::-1], top_5[rate_col][::-1], 
               xerr=top_5['uncertainty'][::-1],
               color='#c0392b', capsize=4, edgecolor='black', alpha=0.85)

ax.set_xlabel(f"Incidence Rate per 100,000 in {target_year} ($\sigma = \sqrt{{R}}$)")
ax.set_title(f"Top 5 Countries by Tuberculosis Incidence ({target_year})")
plt.tight_layout()
fig1_path = os.path.join(FIGURES_DIR, "plot_1.png")
plt.savefig(fig1_path, dpi=300)
plt.close()

# ==========================================
# QUANTITATIVE OUTPUT (For LaTeX Equations)
# ==========================================
c1 = top_5.iloc[0]
c2 = top_5.iloc[1]

r1, sig1 = c1[rate_col], c1['uncertainty']
r2, sig2 = c2[rate_col], c2['uncertainty']
diff = r1 - r2
diff_err = np.sqrt(sig1**2 + sig2**2)

print("\n" + "=" * 60)
print("EQUATION VALUES FOR LATEX REPORT (Section 3):")
print(f"R_1 ({c1['Entity']}): {r1:.2f} +/- {sig1:.2f}")
print(f"R_2 ({c2['Entity']}): {r2:.2f} +/- {sig2:.2f}")
print(f"Delta R (Difference): {diff:.2f} +/- {diff_err:.2f}")
print("=" * 60)

# ==========================================
# FIGURE 2: 2016–2024 Trend & COVID Impact
# ==========================================
top_entity = c1['Entity']
trend_df = cdf[(cdf['Entity'] == top_entity) & (cdf['Year'] >= 2016) & (cdf['Year'] <= target_year)].sort_values('Year')

fig, ax = plt.subplots(figsize=(6.8, 4.0))
ax.plot(trend_df['Year'], trend_df[rate_col], marker='o', linewidth=2, color='#c0392b', label=f'{top_entity}')

# Highlight the COVID-19 pandemic period
ax.axvspan(2019.5, 2021.5, color='#bdc3c7', alpha=0.4, label='COVID-19 Disruption (2020-2021)')

# Annotate the pre- vs post-2020 points
r_2019 = trend_df[trend_df['Year'] == 2019][rate_col].values
r_2020 = trend_df[trend_df['Year'] == 2020][rate_col].values
if len(r_2019) > 0 and len(r_2020) > 0:
    covid_shift = r_2020[0] - r_2019[0]
    print(f"Shift 2019 -> 2020: {covid_shift:.2f} per 100k")

ax.set_xlabel("Year")
ax.set_ylabel("Incidence Rate per 100,000")
ax.set_title(f"Tuberculosis Trajectory Around COVID-19: {top_entity} (2016–{target_year})")
ax.set_xticks(range(2016, target_year + 1))
ax.legend(frameon=True)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
fig2_path = os.path.join(FIGURES_DIR, "plot_2.png")
plt.savefig(fig2_path, dpi=300)
plt.close()

print(f"\nGenerated files:\n- {fig1_path}\n- {fig2_path}\n")