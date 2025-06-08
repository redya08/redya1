
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- LOAD DATA ---
df = pd.read_csv("vgsales.csv")

# --- CLEANING ---
df.dropna(subset=['Year', 'Publisher', 'Genre', 'Global_Sales'], inplace=True)
df['Year'] = df['Year'].astype(int)

# --- SIDEBAR FILTERS ---
st.sidebar.title("🎮 Filter Data")
selected_genre = st.sidebar.multiselect("Pilih Genre:", sorted(df['Genre'].unique()), default=df['Genre'].unique())
selected_year = st.sidebar.slider("Tahun Rilis:", int(df['Year'].min()), int(df['Year'].max()), (2000, 2010))

df_filtered = df[
    (df['Genre'].isin(selected_genre)) &
    (df['Year'].between(selected_year[0], selected_year[1]))
]

# --- TITLE ---
st.title("📊 Dashboard Analisis Penjualan Video Game")
st.markdown("Visualisasi data penjualan game berdasarkan genre, tahun, dan publisher.")

# --- KPI METRICS ---
total_games = df_filtered.shape[0]
total_sales = df_filtered['Global_Sales'].sum()
mean_sales = df_filtered['Global_Sales'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("🎮 Jumlah Game", f"{total_games}")
col2.metric("💰 Total Penjualan (Juta)", f"{total_sales:.2f}")
col3.metric("📈 Rata-rata Penjualan", f"{mean_sales:.2f}")

# --- CHART 1: Top Publisher ---
st.subheader("Top 10 Publisher dengan Penjualan Tertinggi")
top_publishers = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_publishers)

# --- CHART 2: Distribusi Genre (Pie) ---
st.subheader("Distribusi Genre Game")
genre_counts = df_filtered['Genre'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# --- CHART 3: Histogram Penjualan Global ---
st.subheader("Distribusi Penjualan Global")
fig2, ax2 = plt.subplots()
sns.histplot(df_filtered['Global_Sales'], bins=30, kde=True, ax=ax2)
st.pyplot(fig2)

# --- CHART 4: Tren Penjualan per Tahun ---
st.subheader("Tren Total Penjualan Global per Tahun")
trend = df_filtered.groupby('Year')['Global_Sales'].sum()
fig3, ax3 = plt.subplots()
trend.plot(ax=ax3)
ax3.set_ylabel("Global Sales")
st.pyplot(fig3)

# --- CHART 5: Korelasi Antar Variabel Numerik ---
st.subheader("Korelasi Antar Variabel Numerik")
fig4, ax4 = plt.subplots()
sns.heatmap(df_filtered[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].corr(), annot=True, cmap="Blues", ax=ax4)
st.pyplot(fig4)
