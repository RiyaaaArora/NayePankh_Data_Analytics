# 🪁 NayePankh Foundation — Data Analytics Project

> **UP Govt. Registered NGO | 80G & 12A Certified | Est. 28 March 2021**  
> *"If we all do something, then together there is no problem that we cannot solve!"* — Prashant Shukla, Founder

---

## 📌 About This Project

This is a **Data Analytics project** built on publicly available information from [nayepankh.com](https://nayepankh.com), created as part of the **NayePankh Foundation Internship Task**.

It simulates real-world NGO data and performs end-to-end analysis including dashboards, trend forecasting, deep-dive visualizations, and an automated impact report — all in a single Python script.

---

## 🗂️ Repository Structure

```
nayepankh-data-analytics/
│
├── nayepankh_analytics.py       # 🐍 Main Python script (run this)
│
├── outputs/
│   ├── nayepankh_dashboard.png  # 📊 8-panel KPI Dashboard
│   ├── nayepankh_forecast.png   # 📈 12-Month Trend Forecast
│   ├── nayepankh_deepdive.png   # 🔍 Deep-Dive Visualizations
│   ├── nayepankh_report.txt     # 📄 Automated Analytics Report
│   └── nayepankh_data.json      # 💾 Structured Summary (JSON)
│
└── README.md                    # 📖 You are here
```

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/RiyaaaArora/nayepankh-data-analytics.git
cd nayepankh-data-analytics
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 3. Run the Script
```bash
python nayepankh_analytics.py
```

All output files (charts, report, JSON) will be generated in the same folder automatically.

---

## 📊 Features

| Feature | Description |
|---|---|
| 📦 Dataset Generation | Simulated 5 datasets: monthly ops, city-wise, program-wise, volunteers, donations |
| 🔍 EDA | Key metrics: beneficiaries, donations, volunteers, growth rates |
| 📊 Dashboard | 8-panel figure with KPI banner, trends, city breakdown, program pie chart |
| 📈 Forecasting | 12-month polynomial forecasts with 95% confidence bands for all KPIs |
| 🔬 Deep-Dive | Yearly comparisons, heatmaps, role breakdowns, donation distributions |
| 📄 Auto Report | Full text report with stats, insights & recommendations auto-generated |
| 💾 JSON Export | Structured summary data exported for downstream use |

---

## 📉 Key Insights from Analysis

- **2,63,345+** cumulative beneficiaries reached across 6 cities (Mar 2021 – Jun 2026)
- **Volunteers ↔ Beneficiaries correlation: r = 0.981** — confirms the volunteer-driven impact model
- **17.7% YoY growth** in beneficiaries (2024 → 2025)
- **21.3% YoY growth** in donations (2024 → 2025)
- **Kanpur** is the top performing city; **Online Portal** is the #1 donation channel
- Average volunteer age is just **20.6 years** — truly a youth-led movement
- ~35% of donations are recurring — targeting 50% recurring by 2027 is recommended

---

## 🖼️ Output Previews

### 📊 KPI Dashboard
![Dashboard](outputs/nayepankh_dashboard.png)

### 📈 12-Month Forecast
![Forecast](outputs/nayepankh_forecast.png)

### 🔍 Deep-Dive Analysis
![Deep Dive](outputs/nayepankh_deepdive.png)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `Python 3.8+` | Core language |
| `Pandas` | Data manipulation |
| `NumPy` | Numerical computing |
| `Matplotlib` | Charting & dashboards |
| `Seaborn` | Statistical visualizations |
| `SciPy` | Trend fitting & statistics |

---

## 🏢 About NayePankh Foundation

NayePankh Foundation is one of India's biggest student-led NGOs, operating in Kanpur, Ghaziabad, and beyond. Founded on 28 March 2021 by Prashant Shukla during the COVID-19 pandemic, the foundation helps underprivileged communities through:

- 🍱 Free Food Distribution
- 👕 Clothes Drives
- 🩺 Sanitary Napkin Distribution
- 📚 Education Sessions
- 🐾 Animal Welfare

**Registrations:** UP Government | 80G & 12A (Income Tax Act)  
**Website:** [nayepankh.com](https://nayepankh.com)  
**Email:** contact@nayepankh.com

---

## 👤 Author

**Riya Arora**  
NayePankh Foundation — Data Analytics Intern  
[GitHub Profile](https://github.com/RiyaaaArora) | [LinkedIn](https://linkedin.com/in/riyaa-aroraa)

---

*Data sourced from publicly available information at nayepankh.com. Datasets are simulated for analytical demonstration purposes.*
