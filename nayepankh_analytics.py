"""
╔══════════════════════════════════════════════════════════════════╗
║         NayePankh Foundation — Data Analytics Project           ║
║     UP Govt. Registered NGO | 80G & 12A Certified | Est. 2021  ║
╚══════════════════════════════════════════════════════════════════╝

WHAT THIS PROJECT COVERS:
  1. Simulated dataset generation (based on real foundation info)
  2. Exploratory Data Analysis (EDA)
  3. Interactive Dashboard (matplotlib)
  4. Trend Analysis & Forecasting
  5. Automated PDF / Text Report
  6. City-wise & Program-wise breakdowns

Run:  python nayepankh_analytics.py
Requires: pip install pandas numpy matplotlib seaborn scipy
"""

# ─────────────────────────────────────────────
# 0. IMPORTS & SETUP
# ─────────────────────────────────────────────
import os
import json
import random
import warnings
import textwrap
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
random.seed(42)
np.random.seed(42)

# ── Colour Palette (inspired by NayePankh teal/orange branding) ──
BRAND   = "#1A6B72"   # teal-dark
ACCENT  = "#F4A42B"   # amber-orange
LIGHT   = "#D4EEF0"   # pale teal
RED     = "#E05252"
GREEN   = "#3DBE7A"
GREY    = "#8E8E93"
BG      = "#F7FBFC"

CITY_COLORS   = [BRAND, ACCENT, GREEN, RED, "#9B59B6", "#3498DB"]
PROG_COLORS   = [BRAND, ACCENT, GREEN, RED, "#E67E22"]

matplotlib.rcParams.update({
    "font.family":     "DejaVu Sans",
    "axes.facecolor":  BG,
    "figure.facecolor": "white",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
    "axes.titleweight": "bold",
    "axes.titlesize":   13,
    "axes.labelsize":   11,
})

print("=" * 65)
print("  NayePankh Foundation — Data Analytics Engine")
print("  Founded: 28 March 2021 | Kanpur & Ghaziabad, UP")
print("=" * 65)

# ─────────────────────────────────────────────
# 1. DATASET GENERATION
# ─────────────────────────────────────────────
print("\n[1/6]  Generating datasets …")

# ── 1a. Monthly Operations (Mar 2021 – Jun 2026) ──────────────────
months = pd.date_range("2021-03-01", "2026-06-01", freq="MS")

def _growth(n, base, scale, noise=0.12):
    """Logistic growth with noise."""
    x     = np.linspace(0, 6, n)
    logis = base + scale / (1 + np.exp(-1.2 * (x - 2.5)))
    return np.maximum(0, logis + np.random.normal(0, logis * noise))

n = len(months)

food_dist     = _growth(n, 400,  2_200).astype(int)
cloth_dist    = _growth(n, 100,    900).astype(int)
sanitary_dist = _growth(n, 200,  1_600).astype(int)
edu_sessions  = _growth(n,  10,    140).astype(int)
volunteers    = _growth(n,  25,    475).astype(int)
donations_inr = _growth(n, 8_000, 92_000, noise=0.18).astype(int)
beneficiaries = (food_dist + cloth_dist + sanitary_dist +
                 edu_sessions * 8).astype(int)

monthly_df = pd.DataFrame({
    "month":               months,
    "food_packets":        food_dist,
    "clothes_distributed": cloth_dist,
    "sanitary_pads":       sanitary_dist,
    "edu_sessions":        edu_sessions,
    "volunteers":          volunteers,
    "donations_inr":       donations_inr,
    "beneficiaries":       beneficiaries,
})
monthly_df["year"]      = monthly_df["month"].dt.year
monthly_df["month_num"] = monthly_df["month"].dt.month
monthly_df["quarter"]   = monthly_df["month"].dt.to_period("Q").astype(str)

# ── 1b. City-wise Data ────────────────────────────────────────────
cities = ["Kanpur", "Ghaziabad", "Lucknow", "Prayagraj", "Agra", "Varanasi"]
city_share = np.array([0.35, 0.28, 0.15, 0.10, 0.07, 0.05])

total_ben = int(beneficiaries.sum())
city_df = pd.DataFrame({
    "city":          cities,
    "beneficiaries": (city_share * total_ben).astype(int),
    "volunteers":    (city_share * int(volunteers.sum())).astype(int),
    "events_held":   np.random.randint(20, 300, len(cities)),
    "donations_inr": (city_share * int(donations_inr.sum())).astype(int),
})

# ── 1c. Program Breakdown ─────────────────────────────────────────
programs = ["Food Distribution", "Clothes Drive",
            "Sanitary Napkins", "Education", "Animal Welfare"]
prog_share = np.array([0.38, 0.22, 0.20, 0.15, 0.05])

prog_df = pd.DataFrame({
    "program":       programs,
    "beneficiaries": (prog_share * total_ben).astype(int),
    "budget_inr":    (prog_share * int(donations_inr.sum())).astype(int),
    "events":        np.random.randint(50, 600, len(programs)),
    "volunteers":    (prog_share * int(volunteers.sum())).astype(int),
})

# ── 1d. Volunteer Demographics ────────────────────────────────────
n_vol   = 1_200
vol_df  = pd.DataFrame({
    "age":       np.clip(np.random.normal(21, 3.5, n_vol), 16, 35).astype(int),
    "gender":    np.random.choice(["Male", "Female", "Other"],
                                  n_vol, p=[0.52, 0.46, 0.02]),
    "city":      np.random.choice(cities, n_vol, p=city_share),
    "role":      np.random.choice(
                    ["Field Volunteer", "Coordinator", "Social Media",
                     "Fundraiser", "Educator"], n_vol,
                    p=[0.40, 0.20, 0.15, 0.15, 0.10]),
    "hours_pm":  np.clip(np.random.normal(12, 5, n_vol), 2, 40).round(1),
    "joined_yr": np.random.choice([2021, 2022, 2023, 2024, 2025, 2026],
                                  n_vol, p=[0.08,0.18,0.22,0.24,0.20,0.08]),
})

# ── 1e. Donation Records ──────────────────────────────────────────
n_don    = 3_000
don_df   = pd.DataFrame({
    "date":      pd.to_datetime(
                    np.random.choice(monthly_df["month"], n_don) +
                    pd.to_timedelta(np.random.randint(0, 28, n_don), unit="d")),
    "amount":    np.clip(np.random.exponential(1_500, n_don), 100, 50_000).astype(int),
    "source":    np.random.choice(
                    ["Online Portal", "Instagram", "LinkedIn", "Word-of-Mouth",
                     "Corporate", "Events"], n_don,
                    p=[0.30, 0.22, 0.18, 0.15, 0.10, 0.05]),
    "type":      np.random.choice(["One-time", "Recurring"], n_don, p=[0.65, 0.35]),
    "city":      np.random.choice(cities + ["Other"], n_don,
                                  p=[0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.10]),
})

print(f"   ✔  Monthly records  : {len(monthly_df)} months")
print(f"   ✔  Cities tracked   : {len(city_df)}")
print(f"   ✔  Programs tracked : {len(prog_df)}")
print(f"   ✔  Volunteer records: {len(vol_df)}")
print(f"   ✔  Donation records : {len(don_df)}")

# ─────────────────────────────────────────────
# 2. EDA — Key Metrics
# ─────────────────────────────────────────────
print("\n[2/6]  Exploratory Data Analysis …")

total_beneficiaries = int(beneficiaries.sum())
total_donations     = int(donations_inr.sum())
total_volunteers    = int(volunteers.max())          # peak volunteers
total_events        = int(edu_sessions.sum())
yoy_growth          = ((monthly_df[monthly_df.year == 2025]["beneficiaries"].sum() /
                        monthly_df[monthly_df.year == 2024]["beneficiaries"].sum()) - 1) * 100

print(f"\n   ── KEY METRICS ─────────────────────────────")
print(f"   Total Beneficiaries  : {total_beneficiaries:>12,}")
print(f"   Total Donations (₹)  : {total_donations:>12,}")
print(f"   Peak Volunteers      : {total_volunteers:>12,}")
print(f"   Education Sessions   : {total_events:>12,}")
print(f"   YoY Growth (2024→25) : {yoy_growth:>11.1f}%")
print(f"   Cities Active        : {len(cities):>12}")

# ─────────────────────────────────────────────
# 3. DASHBOARD (8-panel figure)
# ─────────────────────────────────────────────
print("\n[3/6]  Building dashboard …")

fig = plt.figure(figsize=(20, 24), facecolor="white")
fig.suptitle(
    "NayePankh Foundation — Impact Analytics Dashboard\n"
    "UP Govt. Registered NGO | Est. 28 March 2021 | 80G & 12A Certified",
    fontsize=17, fontweight="bold", color=BRAND, y=0.995
)

gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.48, wspace=0.35,
                       left=0.06, right=0.97, top=0.96, bottom=0.04)

# ── KPI Banner (row 0) ────────────────────────────────────────────
kpi_ax = fig.add_subplot(gs[0, :])
kpi_ax.set_facecolor(BRAND)
kpi_ax.set_xticks([]); kpi_ax.set_yticks([])
for spine in kpi_ax.spines.values(): spine.set_visible(False)

kpis = [
    ("2,00,000+",  "People Helped"),
    (f"₹{total_donations/1e6:.1f}M",  "Funds Raised"),
    (f"{total_volunteers:,}", "Peak Volunteers"),
    (f"{len(cities)}",        "Active Cities"),
    (f"{total_events:,}",     "Edu. Sessions"),
    ("80G & 12A",             "Tax Certified"),
]
for i, (val, lbl) in enumerate(kpis):
    x = 0.08 + i * 0.155
    kpi_ax.text(x, 0.65, val,  transform=kpi_ax.transAxes,
                fontsize=18, fontweight="bold", color=ACCENT, ha="center", va="center")
    kpi_ax.text(x, 0.22, lbl, transform=kpi_ax.transAxes,
                fontsize=9,  color="white",  ha="center", va="center")
kpi_ax.set_title("", pad=0)

# ── Panel 1 – Monthly Beneficiaries Trend ─────────────────────────
ax1 = fig.add_subplot(gs[1, :2])
ax1.fill_between(monthly_df["month"], monthly_df["beneficiaries"],
                 alpha=0.18, color=BRAND)
ax1.plot(monthly_df["month"], monthly_df["beneficiaries"],
         color=BRAND, lw=2.2, label="Beneficiaries / Month")
# Annotate years
for yr in range(2021, 2027):
    yr_data = monthly_df[monthly_df.year == yr]
    if len(yr_data):
        peak = yr_data.loc[yr_data["beneficiaries"].idxmax()]
        ax1.axvline(pd.Timestamp(f"{yr}-01-01"), color=GREY, lw=0.6, ls=":")
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
ax1.set_title("Monthly Beneficiaries Trend (2021 – 2026)")
ax1.set_xlabel("Month"); ax1.set_ylabel("Beneficiaries")
ax1.legend(loc="upper left", fontsize=9)

# ── Panel 2 – Donations Trend ─────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 2])
monthly_df["roll3"] = monthly_df["donations_inr"].rolling(3).mean()
ax2.bar(monthly_df["month"], monthly_df["donations_inr"],
        width=20, color=ACCENT, alpha=0.4, label="Monthly")
ax2.plot(monthly_df["month"], monthly_df["roll3"],
         color=RED, lw=2, label="3-mo MA")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{int(x/1000)}K"))
ax2.set_title("Monthly Donations (₹)")
ax2.set_xlabel("Month"); ax2.legend(fontsize=8)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")

# ── Panel 3 – City-wise Beneficiaries ─────────────────────────────
ax3 = fig.add_subplot(gs[2, 0])
bars = ax3.barh(city_df["city"], city_df["beneficiaries"],
                color=CITY_COLORS, edgecolor="white", height=0.6)
for bar, val in zip(bars, city_df["beneficiaries"]):
    ax3.text(bar.get_width() + 500, bar.get_y() + bar.get_height() / 2,
             f"{val:,}", va="center", fontsize=8, color=GREY)
ax3.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
ax3.set_title("City-wise Beneficiaries")
ax3.set_xlabel("Beneficiaries")

# ── Panel 4 – Program Breakdown (Pie) ────────────────────────────
ax4 = fig.add_subplot(gs[2, 1])
wedges, texts, autotexts = ax4.pie(
    prog_df["beneficiaries"], labels=prog_df["program"],
    colors=PROG_COLORS, autopct="%1.1f%%", startangle=140,
    textprops={"fontsize": 8}, pctdistance=0.78,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
for at in autotexts: at.set_color("white"); at.set_fontweight("bold")
ax4.set_title("Beneficiaries by Program")

# ── Panel 5 – Volunteer Growth ───────────────────────────────────
ax5 = fig.add_subplot(gs[2, 2])
ax5.fill_between(monthly_df["month"], monthly_df["volunteers"],
                 alpha=0.20, color=GREEN)
ax5.plot(monthly_df["month"], monthly_df["volunteers"],
         color=GREEN, lw=2.2)
ax5.set_title("Volunteer Count Growth")
ax5.set_xlabel("Month"); ax5.set_ylabel("Volunteers")
ax5.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=30, ha="right")

# ── Panel 6 – Volunteer Age Distribution ─────────────────────────
ax6 = fig.add_subplot(gs[3, 0])
ax6.hist(vol_df["age"], bins=20, color=BRAND, alpha=0.75, edgecolor="white")
ax6.axvline(vol_df["age"].mean(), color=ACCENT, lw=2,
            label=f"Mean: {vol_df['age'].mean():.1f} yrs")
ax6.set_title("Volunteer Age Distribution")
ax6.set_xlabel("Age (years)"); ax6.set_ylabel("Count")
ax6.legend(fontsize=9)

# ── Panel 7 – Gender Split ────────────────────────────────────────
ax7 = fig.add_subplot(gs[3, 1])
gcounts = vol_df["gender"].value_counts()
gcolors = [BRAND, ACCENT, GREEN]
ax7.pie(gcounts, labels=gcounts.index, autopct="%1.1f%%",
        colors=gcolors, startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 10})
ax7.set_title("Volunteer Gender Split")

# ── Panel 8 – Donation Source ─────────────────────────────────────
ax8 = fig.add_subplot(gs[3, 2])
src_sum = don_df.groupby("source")["amount"].sum().sort_values()
bars2 = ax8.barh(src_sum.index, src_sum.values,
                 color=[BRAND, ACCENT, GREEN, RED, "#9B59B6", "#3498DB"],
                 edgecolor="white", height=0.6)
ax8.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{int(x/1e6):.1f}M"))
ax8.set_title("Donation by Source (₹)")
ax8.set_xlabel("Total Donations (₹)")

plt.savefig("nayepankh_dashboard.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("   ✔  Dashboard saved → nayepankh_dashboard.png")

# ─────────────────────────────────────────────
# 4. TREND ANALYSIS & FORECAST
# ─────────────────────────────────────────────
print("\n[4/6]  Trend Analysis & Forecasting …")

fig2, axes = plt.subplots(2, 2, figsize=(16, 11), facecolor="white")
fig2.suptitle("NayePankh Foundation — Trend Analysis & 12-Month Forecast",
              fontsize=15, fontweight="bold", color=BRAND)

cols_fcst = ["beneficiaries", "donations_inr", "volunteers", "food_packets"]
titles_f  = ["Beneficiaries", "Donations (₹)", "Volunteers", "Food Packets"]
colors_f  = [BRAND, ACCENT, GREEN, RED]

for ax, col, title, clr in zip(axes.flat, cols_fcst, titles_f, colors_f):
    series = monthly_df[col].values.astype(float)
    t      = np.arange(len(series))

    # Linear + quadratic fit
    deg2 = np.polyfit(t, series, 2)
    p2   = np.poly1d(deg2)

    # Forecast 12 months
    t_fore = np.arange(len(series), len(series) + 12)
    fore   = p2(t_fore)
    fore   = np.maximum(fore, 0)

    # 95% confidence band (simple residual-based)
    resid  = series - p2(t)
    sigma  = resid.std()

    ax.fill_between(t, p2(t) - 1.96 * sigma, p2(t) + 1.96 * sigma,
                    alpha=0.10, color=clr)
    ax.plot(t,      series, color=clr, lw=1.8, alpha=0.7, label="Actual")
    ax.plot(t,      p2(t),  color=clr, lw=1.2, ls="--",  alpha=0.5, label="Trend Fit")
    ax.fill_between(t_fore, fore - 1.96 * sigma, fore + 1.96 * sigma,
                    alpha=0.15, color=clr)
    ax.plot(t_fore, fore, color=clr, lw=2.2, ls="-.", label="Forecast")
    ax.axvline(len(series) - 1, color=GREY, lw=1.2, ls=":")
    ax.text(len(series) - 0.5, ax.get_ylim()[1] * 0.95, "▶ Forecast",
            fontsize=8, color=GREY)

    if col == "donations_inr":
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    else:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

    ax.set_title(f"{title} — 12-Month Forecast")
    ax.set_xlabel("Month Index (0 = Mar 2021)")
    ax.legend(fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("nayepankh_forecast.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("   ✔  Forecast chart saved → nayepankh_forecast.png")

# ─────────────────────────────────────────────
# 5. DEEP-DIVE VISUALIZATIONS
# ─────────────────────────────────────────────
print("\n[5/6]  Deep-dive visualizations …")

fig3, axes3 = plt.subplots(2, 3, figsize=(18, 11), facecolor="white")
fig3.suptitle("NayePankh Foundation — Deep-Dive Analysis",
              fontsize=15, fontweight="bold", color=BRAND)

# 5a. Yearly Program Comparison
ax = axes3[0, 0]
yearly = monthly_df.groupby("year")[
    ["food_packets", "clothes_distributed", "sanitary_pads", "edu_sessions"]
].sum().reset_index()
x = np.arange(len(yearly))
w = 0.20
prog_cols = ["food_packets", "clothes_distributed", "sanitary_pads", "edu_sessions"]
prog_lbls = ["Food", "Clothes", "Sanitary", "Education"]
for i, (c, lbl) in enumerate(zip(prog_cols, prog_lbls)):
    ax.bar(x + i * w, yearly[c], width=w,
           label=lbl, color=PROG_COLORS[i], edgecolor="white")
ax.set_xticks(x + 1.5 * w)
ax.set_xticklabels(yearly["year"])
ax.set_title("Yearly Program Distribution")
ax.set_ylabel("Units Distributed")
ax.legend(fontsize=9)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

# 5b. Quarterly Donations Heatmap
ax = axes3[0, 1]
hm = monthly_df.copy()
hm["Q"]  = hm["month"].dt.quarter
hm["Yr"] = hm["month"].dt.year
pivot = hm.pivot_table(values="donations_inr", index="Yr", columns="Q",
                       aggfunc="sum") / 1_000
sns.heatmap(pivot, ax=ax, cmap="YlOrBr", fmt=".0f", annot=True,
            linewidths=0.5, cbar_kws={"label": "₹K"})
ax.set_title("Quarterly Donations Heatmap (₹K)")
ax.set_xlabel("Quarter"); ax.set_ylabel("Year")

# 5c. Volunteer Role Breakdown
ax = axes3[0, 2]
role_cnt = vol_df["role"].value_counts()
bars = ax.bar(role_cnt.index, role_cnt.values,
              color=CITY_COLORS[:len(role_cnt)], edgecolor="white")
ax.set_title("Volunteer Roles")
ax.set_ylabel("Volunteer Count")
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20, ha="right", fontsize=9)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
            str(int(bar.get_height())), ha="center", fontsize=8)

# 5d. Donation Amount Distribution (log scale)
ax = axes3[1, 0]
ax.hist(don_df["amount"], bins=50, color=BRAND, alpha=0.7, edgecolor="white")
ax.axvline(don_df["amount"].median(), color=ACCENT, lw=2,
           label=f"Median: ₹{int(don_df['amount'].median()):,}")
ax.axvline(don_df["amount"].mean(), color=RED, lw=2, ls="--",
           label=f"Mean: ₹{int(don_df['amount'].mean()):,}")
ax.set_title("Donation Amount Distribution")
ax.set_xlabel("Amount (₹)"); ax.set_ylabel("Frequency")
ax.legend(fontsize=9)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₹{int(x/1000)}K"))

# 5e. Cumulative Beneficiaries
ax = axes3[1, 1]
monthly_df["cum_ben"] = monthly_df["beneficiaries"].cumsum()
ax.fill_between(monthly_df["month"], monthly_df["cum_ben"],
                alpha=0.15, color=GREEN)
ax.plot(monthly_df["month"], monthly_df["cum_ben"], color=GREEN, lw=2.5)
ax.axhline(200_000, color=ACCENT, lw=1.5, ls="--", label="2,00,000 milestone")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
ax.set_title("Cumulative Beneficiaries Reached")
ax.set_xlabel("Month"); ax.set_ylabel("Cumulative Count")
ax.legend(fontsize=9)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")

# 5f. Volunteer Joining Year
ax = axes3[1, 2]
yr_cnt = vol_df["joined_yr"].value_counts().sort_index()
ax.bar(yr_cnt.index.astype(str), yr_cnt.values,
       color=[BRAND, ACCENT, GREEN, RED, "#9B59B6", "#3498DB"],
       edgecolor="white")
ax.set_title("Volunteers Joined by Year")
ax.set_xlabel("Year"); ax.set_ylabel("New Volunteers")
for i, v in enumerate(yr_cnt.values):
    ax.text(i, v + 5, str(v), ha="center", fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("nayepankh_deepdive.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("   ✔  Deep-dive chart saved → nayepankh_deepdive.png")

# ─────────────────────────────────────────────
# 6. AUTOMATED REPORT (TEXT + JSON)
# ─────────────────────────────────────────────
print("\n[6/6]  Generating automated report …")

# ── Statistical correlations ──────────────────────────────────────
corr_vol_ben = monthly_df["volunteers"].corr(monthly_df["beneficiaries"])
corr_don_ben = monthly_df["donations_inr"].corr(monthly_df["beneficiaries"])
top_city     = city_df.loc[city_df["beneficiaries"].idxmax(), "city"]
top_prog     = prog_df.loc[prog_df["beneficiaries"].idxmax(), "program"]
top_source   = don_df.groupby("source")["amount"].sum().idxmax()

# ── 2025 vs 2024 YoY ─────────────────────────────────────────────
d24 = monthly_df[monthly_df.year == 2024]["donations_inr"].sum()
d25 = monthly_df[monthly_df.year == 2025]["donations_inr"].sum()
don_yoy = (d25 / d24 - 1) * 100

report_lines = f"""
╔══════════════════════════════════════════════════════════════════╗
║         NAYEPANKH FOUNDATION — AUTOMATED ANALYTICS REPORT      ║
║                  Generated: {datetime.now().strftime("%d %B %Y, %H:%M")}                  ║
╚══════════════════════════════════════════════════════════════════╝

ABOUT THE ORGANISATION
───────────────────────
Name       : NayePankh Foundation
Founded    : 28 March 2021 (Kanpur, Uttar Pradesh)
Type       : UP Govt. Registered NGO
Certif.    : 80G & 12A (Income Tax Act) — Donations are 50% tax exempt
Mission    : Uplift underprivileged communities through food, clothing,
             sanitary hygiene, education & animal welfare
Founder    : Prashant Shukla (President)
Contact    : contact@nayepankh.com | +91-8318500748
Website    : https://nayepankh.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — CUMULATIVE IMPACT (Mar 2021 – Jun 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Beneficiaries Helped : {total_beneficiaries:>12,}
  Total Donations Raised (₹) : {total_donations:>12,}
  Peak Volunteer Strength    : {total_volunteers:>12,}
  Education Sessions Held    : {total_events:>12,}
  Cities with Active Ops     : {len(cities):>12}
  Total Donation Records     : {len(don_df):>12,}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — PROGRAM-WISE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'Program':<25} {'Beneficiaries':>14} {'Budget (₹)':>14} {'Events':>8}
{'-'*65}"""

for _, row in prog_df.iterrows():
    report_lines += f"\n  {row['program']:<23} {row['beneficiaries']:>14,} {row['budget_inr']:>14,} {row['events']:>8,}"

report_lines += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — CITY-WISE OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'City':<15} {'Beneficiaries':>14} {'Volunteers':>12} {'Donations (₹)':>16}
{'-'*60}"""

for _, row in city_df.sort_values("beneficiaries", ascending=False).iterrows():
    report_lines += f"\n  {row['city']:<13} {row['beneficiaries']:>14,} {row['volunteers']:>12,} {row['donations_inr']:>16,}"

report_lines += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — VOLUNTEER DEMOGRAPHICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Volunteer Records    : {len(vol_df):,}
  Average Age                : {vol_df['age'].mean():.1f} years
  Age Range                  : {vol_df['age'].min()} – {vol_df['age'].max()} years
  Gender Split               : {vol_df['gender'].value_counts().to_dict()}
  Avg. Hours / Month         : {vol_df['hours_pm'].mean():.1f} hrs
  Most Common Role           : {vol_df['role'].value_counts().idxmax()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — DONATION ANALYTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Donations (₹)        : {don_df['amount'].sum():,}
  Average Donation (₹)       : {don_df['amount'].mean():,.0f}
  Median Donation (₹)        : {don_df['amount'].median():,.0f}
  Highest Single Donation(₹) : {don_df['amount'].max():,}
  Top Donation Source        : {top_source}
  Recurring vs One-time      : {don_df['type'].value_counts().to_dict()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6 — TREND & CORRELATION ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Volunteers ↔ Beneficiaries (r): {corr_vol_ben:.3f}  (Strong positive)
  Donations  ↔ Beneficiaries (r): {corr_don_ben:.3f}  (Strong positive)
  YoY Beneficiary Growth 24→25  : {yoy_growth:.1f}%
  YoY Donation Growth 24→25     : {don_yoy:.1f}%
  Top Performing City           : {top_city}
  Top Performing Program        : {top_prog}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7 — KEY INSIGHTS & RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅  1. The organisation shows consistent logistic growth — volunteer
          count and beneficiaries are strongly correlated (r≈{corr_vol_ben:.2f}),
          confirming the volunteer-driven impact model.

  ✅  2. {top_city} is the strongest city — directing additional
          resources and replicating its model in smaller cities can
          accelerate national impact.

  ✅  3. {top_source} is the highest-grossing donation channel.
          Increasing digital fundraising campaigns on LinkedIn & Instagram
          can further grow the donation base.

  ✅  4. ~35% of donations are recurring, which builds financial
          stability. Targeting 50% recurring donations by 2027 is
          a realistic and impactful goal.

  ✅  5. Volunteers have an average age of {vol_df['age'].mean():.0f} years — a very young
          base. Structured mentorship and certification programs can
          improve retention and deepen engagement.

  ✅  6. The 12-month forecast projects continued upward growth in
          all KPIs. Expanding to 3 additional tier-2 UP cities in
          FY 2026–27 is strongly supported by the data.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FILES GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊  nayepankh_dashboard.png  — 8-panel KPI dashboard
  📈  nayepankh_forecast.png   — 12-month trend forecasts
  🔍  nayepankh_deepdive.png   — Volunteer & donation deep-dive
  📄  nayepankh_report.txt     — This automated report
  💾  nayepankh_data.json      — Structured summary data (JSON)
  🐍  nayepankh_analytics.py   — Full Python source code

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Data based on publicly available info from nayepankh.com
  Simulated datasets for analytical demonstration purposes.
  "Service to mankind is the service to God." — NayePankh Foundation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

with open("nayepankh_report.txt", "w", encoding="utf-8") as f:
    f.write(report_lines)
print("   ✔  Report saved → nayepankh_report.txt")

# ── JSON summary ──────────────────────────────────────────────────
summary_json = {
    "organisation":    "NayePankh Foundation",
    "founded":         "28 March 2021",
    "location":        "Kanpur & Ghaziabad, UP, India",
    "registration":    "UP Govt. | 80G & 12A",
    "total_beneficiaries": total_beneficiaries,
    "total_donations_inr": total_donations,
    "peak_volunteers":     total_volunteers,
    "edu_sessions":        total_events,
    "active_cities":       len(cities),
    "yoy_growth_pct":      round(yoy_growth, 2),
    "city_data": city_df.to_dict("records"),
    "program_data": prog_df.to_dict("records"),
    "generated_at": datetime.now().isoformat(),
}
with open("nayepankh_data.json", "w") as f:
    json.dump(summary_json, f, indent=2, default=str)
print("   ✔  JSON summary saved → nayepankh_data.json")

print("\n" + "=" * 65)
print("  ✅  ALL DONE! Files saved to output directory.")
print("=" * 65)
print(report_lines)