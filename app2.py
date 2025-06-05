
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("vgsales.csv")

st.title("Dashboard Analisis Video Game Sales")
st.dataframe(df)

# Statistik Deskriptif
st.subheader("Statistik Deskriptif - Numerik")
st.dataframe(df.describe())

st.subheader("Statistik Deskriptif - Kategorikal")
st.dataframe(df.describe(include=['object']))

# Top 10 Publisher
st.subheader("Top 10 Publisher Berdasarkan Jumlah Game")
top_publishers = df['Publisher'].value_counts().head(10)
st.bar_chart(top_publishers)

# Top 10 Genre
st.subheader("Top 10 Genre Paling Umum")
top_genres = df['Genre'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_genres.plot(kind='barh', ax=ax2, color='skyblue')
ax2.set_title('Top 10 Genre Video Game')
st.pyplot(fig2)

# Penjualan Global per Tahun
st.subheader("Total Global Sales per Tahun")
sales_by_year = df.groupby('Year')['Global_Sales'].sum().sort_index()
fig3, ax3 = plt.subplots()
sales_by_year.plot(ax=ax3)
ax3.set_title('Total Global Sales per Tahun')
ax3.set_xlabel('Tahun')
ax3.set_ylabel('Penjualan Global')
st.pyplot(fig3)

# Heatmap Korelasi Numerik
st.subheader("Korelasi antara Kolom Numerik")
corr = df.corr(numeric_only=True)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)
