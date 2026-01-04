# ============================================
# Week 4: Data Visualization & Complete Project
# ============================================

# ---- Backend & Imports (CRITICAL ORDER) ----
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for Windows safety

import os
import pandas as pd
import matplotlib.pyplot as plt

plt.ioff()  # Turn off interactive mode

# ---- Folder Setup ----
os.makedirs("data", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# ---- Load Data ----
DATA_PATH = "data/sales_data.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("sales_data.csv not found in data/ folder")

df = pd.read_csv(DATA_PATH)

# ---- Basic Inspection (Optional for logs) ----
print("Columns:", df.columns.tolist())
print("Initial rows:", len(df))

# ---- Data Cleaning ----

# Convert Total_Sales to numeric
df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop rows with critical missing values
df = df.dropna(subset=["Product", "Region", "Total_Sales", "Date"])

print("Rows after cleaning:", len(df))

# ---- Feature Engineering ----
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# =====================================================
# 1️⃣ BAR CHART: TOTAL SALES BY PRODUCT
# =====================================================
product_sales = (
    df.groupby("Product", as_index=False)["Total_Sales"]
      .sum()
)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(product_sales["Product"], product_sales["Total_Sales"])

ax.set_title("Total Sales by Product")
ax.set_xlabel("Product")
ax.set_ylabel("Total Sales")
plt.setp(ax.get_xticklabels(), rotation=45)

fig.tight_layout()
fig.savefig("visualizations/sales_by_product.png")
plt.close(fig)

print("Saved: sales_by_product.png")

# =====================================================
# 2️⃣ LINE CHART: MONTHLY SALES TREND
# =====================================================
monthly_sales = (
    df.groupby("Month", as_index=False)["Total_Sales"]
      .sum()
      .sort_values("Month")
)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    monthly_sales["Month"],
    monthly_sales["Total_Sales"],
    marker="o"
)

ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")

fig.tight_layout()
fig.savefig("visualizations/monthly_sales_trend.png")
plt.close(fig)

print("Saved: monthly_sales_trend.png")

# =====================================================
# 3️⃣ PIE CHART: SALES DISTRIBUTION BY REGION
# =====================================================
region_sales = (
    df.groupby("Region", as_index=False)["Total_Sales"]
      .sum()
)

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    region_sales["Total_Sales"],
    labels=region_sales["Region"],
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title("Sales Distribution by Region")

fig.tight_layout()
fig.savefig("visualizations/sales_by_region.png")
plt.close(fig)

print("Saved: sales_by_region.png")

# ---- Completion Message ----
print("Week 4 analysis completed successfully.")
