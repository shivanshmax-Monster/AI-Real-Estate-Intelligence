import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic styling
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({'font.size': 10, 'figure.autolayout': True})

os.makedirs("assets", exist_ok=True)
df = pd.read_csv("housing_data.csv")
df["Price_Per_SqFt"] = (df["Price"] / df["Square_Footage"]).round(2)

# 1. KPI & Valuation Distribution Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=df, x="Location_Tier", y="Price", palette="Blues_r", ax=ax1)
ax1.set_title("Market Valuation Spectrum by Location Tier", fontsize=12, fontweight="bold")
ax1.set_xlabel("Location Tier", fontweight="bold")
ax1.set_ylabel("Price ($ USD)", fontweight="bold")
ax1.tick_params(axis='x', rotation=20)

df["Condition"].value_counts().plot.pie(
    autopct="%1.1f%%", colors=["#2563EB", "#10B981", "#F59E0B", "#EF4444"], ax=ax2, startangle=140
)
ax2.set_ylabel("")
ax2.set_title("Inventory Condition Breakdown", fontsize=12, fontweight="bold")
plt.savefig("assets/ui_kpi_distribution.png", dpi=200)
plt.close()

# 2. EDA: Square Footage vs Price with Location Overlay
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=df, x="Square_Footage", y="Price",
    hue="Location_Tier", alpha=0.75, palette="tab10", s=60, ax=ax
)
ax.set_title("Living Area (Sq.Ft) vs. Realized Market Valuation", fontsize=12, fontweight="bold")
ax.set_xlabel("Living Area (Sq.Ft)", fontweight="bold")
ax.set_ylabel("Transaction Price ($ USD)", fontweight="bold")
plt.savefig("assets/ui_eda_sqft_price.png", dpi=200)
plt.close()

# 3. Correlation Matrix Heatmap
num_cols = ["Square_Footage", "Bedrooms", "Bathrooms", "Property_Age_Years", "Distance_to_City_Miles", "Renovation_Score", "Price"]
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=1.0, ax=ax, cbar_kws={'label': 'Correlation Coefficient'})
ax.set_title("Key Valuation Drivers Correlation Matrix", fontsize=12, fontweight="bold")
plt.savefig("assets/ui_correlation_matrix.png", dpi=200)
plt.close()

# 4. Model Performance Benchmark Comparison
models = ["Gradient Boosting", "Random Forest", "Ridge Regression", "Linear Regression"]
r2_scores = [0.9789, 0.9687, 0.9747, 0.9746]
mae_values = [27157.61, 34197.77, 31529.34, 31650.10]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
colors = ["#10B981", "#3B82F6", "#6366F1", "#8B5CF6"]

bars1 = ax1.bar(models, [s * 100 for s in r2_scores], color=colors, width=0.55)
ax1.set_ylim(90, 100)
ax1.set_title("Model Precision Comparison (R² Score %)", fontsize=11, fontweight="bold")
ax1.set_ylabel("R² Accuracy (%)", fontweight="bold")
ax1.tick_params(axis='x', rotation=15)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f"{yval:.2f}%", ha='center', va='bottom', fontweight='bold', fontsize=9)

bars2 = ax2.bar(models, mae_values, color=colors, width=0.55)
ax2.set_title("Mean Absolute Error (Lower is Better)", fontsize=11, fontweight="bold")
ax2.set_ylabel("MAE ($ USD)", fontweight="bold")
ax2.tick_params(axis='x', rotation=15)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 500, f"${yval:,.0f}", ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.savefig("assets/ui_model_benchmarks.png", dpi=200)
plt.close()

# 5. Business Intelligence Hierarchy Visual Diagram
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.axis("off")

stages = [
    ("LEVEL 1: KPIs", "What is Happening?", "$613,353 Median Price | $291.8/SqFt | 1,200 Active Units | 4.8% YoY Appreciation", "#1E3A8A"),
    ("LEVEL 2: Trends", "Where is it Going?", "Quarterly transaction momentum steady (+3.1% QoQ); suburban demand shifting to tech corridors.", "#1D4ED8"),
    ("LEVEL 3: Drivers", "Why is it Happening?", "Living SqFt (+0.82 corr), Location Tier (+45% metro premium), and Renovation Score (+0.36 corr).", "#2563EB"),
    ("LEVEL 4: Risks & Ops", "What Could Go Wrong?", "Risk: Exurban price compression & high flip renovation costs.\nOpportunity: Tech corridor 3-bed units & cosmetic renovations (2.5x ROI).", "#0284C7"),
    ("LEVEL 5: Action", "What Should We Do?", "Deploy 45% capital to Tech Corridors; Cap renovation packages at $18k; Cease >25mi exurban bets.", "#0D9488"),
]

for i, (lvl, q, desc, col) in enumerate(stages):
    y_pos = 0.85 - i * 0.18
    # Header box
    rect = plt.Rectangle((0.02, y_pos - 0.05), 0.28, 0.13, transform=ax.transAxes, color=col, ec="none")
    ax.add_patch(rect)
    ax.text(0.04, y_pos + 0.03, lvl, transform=ax.transAxes, color="white", fontweight="bold", fontsize=11)
    ax.text(0.04, y_pos - 0.02, q, transform=ax.transAxes, color="#BFDBFE", fontstyle="italic", fontsize=9)

    # Content box
    rect_c = plt.Rectangle((0.32, y_pos - 0.05), 0.66, 0.13, transform=ax.transAxes, color="#F8FAFC", ec="#CBD5E1", lw=1.2)
    ax.add_patch(rect_c)
    ax.text(0.34, y_pos + 0.01, desc, transform=ax.transAxes, color="#1E293B", fontsize=9.2, va="center")

plt.savefig("assets/ui_bi_hierarchy.png", dpi=200)
plt.close()

print("[+] All dashboard UI visual screenshots successfully generated in ./assets directory.")
