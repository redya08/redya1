
[theme]
primaryColor = "#00adb5"           # Warna aksen: biru kehijauan terang
backgroundColor = "#222831"        # Latar belakang utama: hitam keabu-abuan
secondaryBackgroundColor = "#393e46"  # Latar belakang sidebar: abu gelap
textColor = "#eeeeee"              # Warna teks: putih terang
font = "sans serif"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURASI LAYOUT & TEMA ---
st.set_page_config(page_title="Dashboard Penjualan Video Game", layout="wide")

# --- LOAD DATA ---
df = pd.read_csv("vgsales.csv")

# --- CLEANING ---
df.dropna(subset=['Year', 'Publisher', 'Genre', 'Global_Sales', 'Platform'], inplace=True)
df['Year'] = df['Year'].astype(int)

# --- SIDEBAR FILTERS ---
st.sidebar.title("🎮 Filter Data")
selected_genre = st.sidebar.multiselect("Pilih Genre:", sorted(df['Genre'].unique()), default=df['Genre'].unique())
selected_year = st.sidebar.slider("Tahun Rilis:", int(df['Year'].min()), int(df['Year'].max()), (2000, 2010))
selected_publisher = st.sidebar.selectbox("Pilih Publisher:", sorted(df['Publisher'].unique()))

df_filtered = df[
    (df['Genre'].isin(selected_genre)) &
    (df['Year'].between(selected_year[0], selected_year[1]))
]

# --- TITLE ---
st.title("📊 Dashboard Penjualan Video Game")
st.markdown("Dashboard ini menampilkan analisis data penjualan game berdasarkan genre, tahun, platform, dan publisher.")

# --- KPI METRICS ---
total_games = df_filtered.shape[0]
total_sales = df_filtered['Global_Sales'].sum()
mean_sales = df_filtered['Global_Sales'].mean()
median_sales = df_filtered['Global_Sales'].median()
std_sales = df_filtered['Global_Sales'].std()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🎮 Jumlah Game", f"{total_games}")
col2.metric("💰 Total Penjualan", f"{total_sales:.2f} juta")
col3.metric("📈 Rata-rata", f"{mean_sales:.2f}")
col4.metric("📊 Median", f"{median_sales:.2f}")
col5.metric("📉 Std Deviasi", f"{std_sales:.2f}")

# --- CHART 1: Top 10 Publisher ---
st.subheader("🏆 Top 10 Publisher berdasarkan Total Penjualan")
top_publishers = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_publishers)

# --- CHART 2: Distribusi Genre (Bar Horizontal) ---
st.subheader("📚 Distribusi Genre Game")
genre_counts = df_filtered['Genre'].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(y=genre_counts.index, x=genre_counts.values, ax=ax1)
ax1.set_xlabel("Jumlah Game")
ax1.set_ylabel("Genre")
st.pyplot(fig1)

# --- CHART 3: Genre dengan Rata-rata Penjualan Tertinggi ---
st.subheader("🔥 Genre dengan Rata-rata Penjualan Tertinggi")
genre_avg_sales = df_filtered.groupby('Genre')['Global_Sales'].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
sns.barplot(x=genre_avg_sales.values, y=genre_avg_sales.index, ax=ax2)
ax2.set_xlabel("Rata-rata Penjualan")
ax2.set_ylabel("Genre")
st.pyplot(fig2)

# --- CHART 4: Platform dengan Total Penjualan Tertinggi ---
st.subheader("🕹️ Platform Paling Populer")
platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)
fig3, ax3 = plt.subplots()
sns.barplot(x=platform_sales.values, y=platform_sales.index, ax=ax3)
ax3.set_xlabel("Total Penjualan")
ax3.set_ylabel("Platform")
st.pyplot(fig3)

# --- CHART 5: Histogram Penjualan Global ---
st.subheader("📦 Distribusi Penjualan Global")
fig4, ax4 = plt.subplots()
sns.histplot(df_filtered['Global_Sales'], bins=30, kde=True, ax=ax4)
ax4.set_xlabel("Global Sales (Juta Unit)")
st.pyplot(fig4)

# --- CHART 6: Tren Penjualan Global per Tahun ---
st.subheader("📅 Tren Penjualan Global per Tahun")
trend = df_filtered.groupby('Year')['Global_Sales'].sum()
fig5, ax5 = plt.subplots()
trend.plot(ax=ax5)
ax5.set_ylabel("Total Penjualan Global")
st.pyplot(fig5)

# --- CHART 7: Korelasi Penjualan Regional ---
st.subheader("🔗 Korelasi Penjualan Regional")
fig6, ax6 = plt.subplots()
sns.heatmap(df_filtered[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].corr(), annot=True, cmap="Blues", ax=ax6)
st.pyplot(fig6)

# --- CHART 8: Tren Penjualan Publisher Tertentu ---
st.subheader(f"📈 Tren Penjualan Global dari Publisher: {selected_publisher}")
pub_trend = df[df['Publisher'] == selected_publisher].groupby('Year')['Global_Sales'].sum()
fig7, ax7 = plt.subplots()
pub_trend.plot(ax=ax7, marker='o', color='green')
ax7.set_ylabel("Total Penjualan")
st.pyplot(fig7)

# --- DOWNLOAD BUTTON ---
st.sidebar.markdown("---")
st.sidebar.download_button("⬇️ Download Data Tersaring (CSV)", data=df_filtered.to_csv(index=False), file_name="filtered_vgsales.csv", mime="text/csv")
