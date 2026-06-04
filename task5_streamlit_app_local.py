"""
Task 5: Global Superstore — Interactive Streamlit Dashboard
============================================================

"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend — safe for Streamlit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ── Must be FIRST Streamlit call ──────────────────────────────────────────────
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom dark CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1rem; padding-bottom: 1rem; }
  [data-testid="metric-container"] {
      background-color: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 10px 16px;
  }
  [data-testid="stSidebar"] { background-color: #161b22; }
</style>
""", unsafe_allow_html=True)


# ── Data generation (cached so it only runs once) ─────────────────────────────
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 9994
    categories = ["Technology", "Furniture", "Office Supplies"]
    subcats = {
        "Technology":      ["Phones", "Copiers", "Machines", "Accessories"],
        "Furniture":       ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Appliances", "Supplies"],
    }
    first = ["John","Mary","James","Patricia","Robert","Jennifer","Michael",
             "Linda","William","Barbara","David","Susan","Richard","Jessica",
             "Thomas","Karen","Christopher","Nancy","Charles","Lisa"]
    last  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller",
             "Davis","Wilson","Anderson","Taylor","Thomas","Jackson","White"]

    rows = []
    base_date = pd.Timestamp("2017-01-01")
    for i in range(n):
        region = np.random.choice(["West","East","Central","South"], p=[0.32,0.28,0.22,0.18])
        cat    = np.random.choice(categories, p=[0.37,0.32,0.31])
        subcat = np.random.choice(subcats[cat])
        seg    = np.random.choice(["Consumer","Corporate","Home Office"], p=[0.52,0.30,0.18])
        ship   = np.random.choice(["Standard Class","Second Class","First Class","Same Day"],
                                  p=[0.60,0.19,0.15,0.06])
        customer = f"{np.random.choice(first)} {np.random.choice(last)}"
        odate  = base_date + pd.Timedelta(days=int(np.random.randint(0, 1461)))
        base_p = {"Technology": 250, "Furniture": 350, "Office Supplies": 30}[cat]
        qty    = int(np.random.randint(1, 10))
        disc   = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5], p=[0.5,0.2,0.15,0.1,0.05])
        sales  = round(abs(np.random.normal(base_p, base_p * 0.4)) * qty * (1 - disc), 2)
        margin = {"Technology":0.18,"Furniture":0.05,"Office Supplies":0.22}[cat]
        if disc > 0.3:
            margin -= 0.15
        profit = round(sales * np.random.normal(margin, 0.05), 2)
        rows.append({
            "Order Date": odate, "Ship Mode": ship, "Customer Name": customer,
            "Segment": seg, "Region": region, "Category": cat,
            "Sub-Category": subcat, "Sales": sales, "Quantity": qty,
            "Discount": disc, "Profit": profit,
        })

    df = pd.DataFrame(rows)
    df["Year"]  = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["YM"]    = df["Order Date"].dt.to_period("M").astype(str)
    return df

df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔧 Dashboard Filters")

def opts(col, all_label="All"):
    return [all_label] + sorted(df_full[col].unique().tolist())

sel_region  = st.sidebar.selectbox("🗺  Region",   opts("Region"))
sel_cat     = st.sidebar.selectbox("📦  Category", opts("Category"))

sub_pool = df_full["Sub-Category"].unique() if sel_cat == "All" \
           else df_full[df_full["Category"] == sel_cat]["Sub-Category"].unique()
sel_sub  = st.sidebar.selectbox("🔍  Sub-Category", ["All"] + sorted(sub_pool.tolist()))

sel_seg  = st.sidebar.selectbox("👤  Segment", opts("Segment"))
sel_year = st.sidebar.selectbox("📅  Year",    ["All"] + sorted(df_full["Year"].unique().tolist()))

# Apply filters
df = df_full.copy()
if sel_region != "All": df = df[df["Region"]       == sel_region]
if sel_cat    != "All": df = df[df["Category"]     == sel_cat]
if sel_sub    != "All": df = df[df["Sub-Category"] == sel_sub]
if sel_seg    != "All": df = df[df["Segment"]      == sel_seg]
if sel_year   != "All": df = df[df["Year"]         == sel_year]

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🌐 Global Superstore — Business Intelligence Dashboard")
st.caption(
    f"Filtered: **{len(df):,} orders**  |  "
    f"Region: {sel_region}  |  Category: {sel_cat}  |  "
    f"Segment: {sel_seg}  |  Year: {sel_year}"
)
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
tot_sales  = df["Sales"].sum()
tot_profit = df["Profit"].sum()
tot_orders = len(df)
margin_pct = tot_profit / tot_sales if tot_sales else 0
avg_order  = tot_sales / tot_orders if tot_orders else 0

k1.metric("💰 Total Sales",     f"${tot_sales:,.0f}")
k2.metric("📈 Total Profit",    f"${tot_profit:,.0f}")
k3.metric("📦 Total Orders",    f"{tot_orders:,}")
k4.metric("🎯 Profit Margin",   f"{margin_pct:.1%}")
k5.metric("🛒 Avg Order Value", f"${avg_order:,.0f}")
st.divider()

# ── Chart helpers ─────────────────────────────────────────────────────────────
DARK, PANEL = "#0d1117", "#161b22"
C = ["#58a6ff","#3fb950","#ffa657","#d2a8ff","#f78166"]

def styled_fig(w=12, h=3.8):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=DARK)
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values(): sp.set_edgecolor("#30363d")
    ax.tick_params(colors="#8b949e", labelsize=8)
    ax.grid(alpha=0.12, color="#21262d")
    return fig, ax

# ── Row 1: Monthly Trend + Region Bar ────────────────────────────────────────
col_l, col_r = st.columns([3, 1])

with col_l:
    st.subheader("📅 Monthly Sales & Profit Trend")
    monthly = (df.groupby("YM")
                 .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
                 .reset_index())
    fig, ax = styled_fig(12, 3.8)
    x = range(len(monthly))
    ax.fill_between(x, monthly["Sales"], alpha=0.12, color=C[0])
    ax.plot(x, monthly["Sales"], color=C[0], lw=2, marker="o", ms=3, label="Sales")
    ax2 = ax.twinx()
    ax2.plot(x, monthly["Profit"], color=C[1], lw=2, ls="--", marker="s", ms=3, label="Profit")
    ax2.set_facecolor(PANEL)
    ax2.tick_params(colors="#8b949e", labelsize=8)
    for sp in ax2.spines.values(): sp.set_edgecolor("#30363d")
    step = max(1, len(monthly) // 12)
    ax.set_xticks(list(x)[::step])
    ax.set_xticklabels(monthly["YM"].values[::step], rotation=45, ha="right",
                       fontsize=7.5, color="#8b949e")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    l1, lb1 = ax.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax.legend(l1+l2, lb1+lb2, facecolor="#1e2430", labelcolor="white", fontsize=9)
    ax.set_ylabel("Sales", color="#8b949e", fontsize=9)
    ax2.set_ylabel("Profit", color="#8b949e", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col_r:
    st.subheader("🗺 By Region")
    rp = df.groupby("Region")["Sales"].sum().sort_values()
    fig, ax = styled_fig(4, 3.8)
    ax.barh(rp.index, rp.values, color=C[:len(rp)], alpha=0.85, height=0.6)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    for i, v in enumerate(rp.values):
        ax.text(v + rp.values.max()*0.01, i, f"${v:,.0f}", va="center",
                color="white", fontsize=8)
    ax.tick_params(axis="y", colors="white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 2: Top 5 Customers + Category Profit + Segment Donut ─────────────────
col_a, col_b, col_c = st.columns([1.4, 1, 1])

with col_a:
    st.subheader("👥 Top 5 Customers by Sales")
    top5 = (df.groupby("Customer Name")["Sales"].sum()
              .reset_index().sort_values("Sales", ascending=False).head(5))
    fig, ax = styled_fig(6, 3.5)
    ax.barh(top5["Customer Name"][::-1], top5["Sales"][::-1],
            color=C[:5], alpha=0.85, height=0.55)
    for bar in ax.patches:
        ax.text(bar.get_width() + top5["Sales"].max()*0.01,
                bar.get_y() + bar.get_height()/2,
                f"${bar.get_width():,.0f}", va="center", color="white", fontsize=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}"))
    ax.tick_params(axis="y", colors="white")
    ax.tick_params(axis="x", colors="#8b949e")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col_b:
    st.subheader("📦 Profit by Category")
    cp = df.groupby("Category").agg(Sales=("Sales","sum"),
                                     Profit=("Profit","sum")).reset_index()
    fig, ax = styled_fig(5, 3.5)
    bar_c = [C[1] if p > 0 else C[4] for p in cp["Profit"]]
    bars = ax.bar(cp["Category"], cp["Profit"], color=bar_c, alpha=0.85)
    ax.axhline(0, color="#555", lw=0.8)
    for bar in bars:
        ypos = bar.get_height() + (cp["Profit"].abs().max()*0.03
                                    if bar.get_height() >= 0
                                    else -cp["Profit"].abs().max()*0.08)
        ax.text(bar.get_x() + bar.get_width()/2, ypos,
                f"${bar.get_height()/1e3:.0f}K",
                ha="center", color="white", fontsize=8.5, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    ax.set_xticklabels(cp["Category"], rotation=12, ha="right",
                       color="white", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col_c:
    st.subheader("👤 Sales by Segment")
    sp2 = df.groupby("Segment")["Sales"].sum()
    fig, ax = styled_fig(5, 3.5)
    wedges, texts, at2 = ax.pie(
        sp2.values, labels=sp2.index,
        colors=[C[0], C[3], C[2]],
        autopct="%1.1f%%", startangle=140,
        pctdistance=0.78,
        wedgeprops={"edgecolor": DARK, "linewidth": 2.5, "width": 0.55})
    for t in texts:  t.set_color("white"); t.set_fontsize(9)
    for a in at2:    a.set_color("white"); a.set_fontsize(8.5)
    ax.set_facecolor(PANEL)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 3: Sub-Category + Discount Analysis ───────────────────────────────────
col_d, col_e = st.columns([1.8, 1])

with col_d:
    st.subheader("🔍 Top 10 Sub-Categories — Sales vs Profit")
    sub = (df.groupby("Sub-Category")
             .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
             .reset_index().sort_values("Sales", ascending=False).head(10))
    fig, ax = styled_fig(10, 3.8)
    x6 = np.arange(len(sub))
    b1 = ax.bar(x6 - 0.2, sub["Sales"],  0.35, label="Sales",  color=C[0], alpha=0.85)
    ax2 = ax.twinx()
    ax2.bar(x6 + 0.2, sub["Profit"], 0.35, label="Profit",
            color=[C[1] if p > 0 else C[4] for p in sub["Profit"]], alpha=0.85)
    ax.set_xticks(x6)
    ax.set_xticklabels(sub["Sub-Category"], rotation=30, ha="right",
                       fontsize=8, color="white")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
    ax2.set_facecolor(PANEL)
    ax2.tick_params(colors="#8b949e", labelsize=8)
    for sp in ax2.spines.values(): sp.set_edgecolor("#30363d")
    ax.legend(facecolor="#1e2430", labelcolor="white", fontsize=8, loc="upper right")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col_e:
    st.subheader("🏷 Avg Profit by Discount Level")
    bins   = [-0.01, 0, 0.1, 0.2, 0.3, 0.6]
    labels = ["0%", "1-10%", "11-20%", "21-30%", "31-60%"]
    df2 = df.copy()
    df2["disc_band"] = pd.cut(df2["Discount"], bins=bins, labels=labels)
    dp = df2.groupby("disc_band", observed=True)["Profit"].mean().reset_index()
    fig, ax = styled_fig(5, 3.8)
    bar_c2 = [C[1] if v > 0 else C[4] for v in dp["Profit"]]
    ax.bar(dp["disc_band"].astype(str), dp["Profit"], color=bar_c2, alpha=0.85)
    ax.axhline(0, color="#555", lw=0.8)
    for i, (_, row) in enumerate(dp.iterrows()):
        ypos = row["Profit"] + (abs(dp["Profit"]).max()*0.04
                                if row["Profit"] >= 0
                                else -abs(dp["Profit"]).max()*0.1)
        ax.text(i, ypos, f"${row['Profit']:,.0f}",
                ha="center", color="white", fontsize=8.5, fontweight="bold")
    ax.set_xticklabels(labels, rotation=15, ha="right", color="white", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Raw Data Table ────────────────────────────────────────────────────────────
st.divider()
with st.expander("📋 View Filtered Raw Data (top 200 rows)"):
    show = df[["Order Date","Region","Category","Sub-Category",
               "Segment","Customer Name","Sales","Profit",
               "Quantity","Discount"]].head(200)
    st.dataframe(
        show.style.format({
            "Sales":    "${:.2f}",
            "Profit":   "${:.2f}",
            "Discount": "{:.0%}",
        }),
        use_container_width=True, height=320,
    )

st.caption(
    f"Global Superstore Dataset  |  {len(df_full):,} total orders  |  2017–2020  |  "
    "Built with Python & Streamlit"
)