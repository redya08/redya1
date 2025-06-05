
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
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
fig1, ax1 = plt.subplots()
top_publishers.plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Publishers by Number of Games')
st.pyplot(fig1)
