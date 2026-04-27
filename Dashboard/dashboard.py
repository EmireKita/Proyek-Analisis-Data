import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Tambahan kolom jika belum ada
    if 'year' not in df.columns:
        df['year'] = df['dteday'].dt.year
        
    return df

df = load_data()

# ========================
# SIDEBAR
# ========================
st.sidebar.title("🔍 Filter")

# Filter tahun
year_options = ["All"] + sorted(df['year'].unique().tolist())
year = st.sidebar.selectbox("Pilih Tahun", year_options)

# Filter bulan
month_range = st.sidebar.slider("Rentang Bulan", 1, 12, (1,12))

if year == "All":
    filtered_df = df[
        (df['mnth'] >= month_range[0]) &
        (df['mnth'] <= month_range[1])
    ]
else:
    filtered_df = df[
        (df['year'] == year) &
        (df['mnth'] >= month_range[0]) &
        (df['mnth'] <= month_range[1])
    ]

# ========================
# HEADER
# ========================
st.title("🚴 Bike Sharing Dashboard")
if year == "All":
    st.markdown("📈 Monitoring tren penyewaan sepeda & pengaruh cuaca (2011-2012)")
else:
    st.markdown(f"📈 Monitoring tren penyewaan sepeda & pengaruh cuaca {year}")
    
# ========================
# DATA PREVIEW
# ========================
with st.expander("🔍 Lihat Data"):
    st.dataframe(filtered_df.head())

# ========================
# METRICS
# ========================
st.subheader("📊 Ringkasan")

col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Rental", int(filtered_df['cnt'].mean()))
col2.metric("Max Rental", int(filtered_df['cnt'].max()))
col3.metric("Min Rental", int(filtered_df['cnt'].min()))

# ========================
# TREN PENYEWAAN
# ========================
st.subheader("📈 Tren Penyewaan Harian")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(filtered_df['dteday'], filtered_df['cnt'])
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# ========================
# RATA-RATA BULANAN
# ========================
st.subheader("📊 Rata-rata Penyewaan per Bulan")

monthly_avg = filtered_df.groupby('mnth')['cnt'].mean()

fig, ax = plt.subplots()
monthly_avg.plot(marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# ========================
# MUSIM
# ========================
st.subheader("🌍 Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots()
sns.boxplot(x='season', y='cnt', data=filtered_df, ax=ax)
st.pyplot(fig)

# ========================
# KORELASI CUACA
# ========================
st.subheader("🌦️ Korelasi Cuaca")

corr = filtered_df[['cnt','temp','hum','windspeed']].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# ========================
# SUHU VS RENTAL
# ========================
st.subheader("🌡️ Suhu vs Penyewaan")

fig, ax = plt.subplots()
sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=ax)
st.pyplot(fig)

# ========================
# HUMIDITY VS RENTAL
# ========================
st.subheader("💧 Kelembaban vs Penyewaan")

fig, ax = plt.subplots()
sns.scatterplot(x='hum', y='cnt', data=filtered_df, ax=ax)
st.pyplot(fig)

# ========================
# DEMAND CLUSTER
# ========================
if 'demand_cluster' in filtered_df.columns:
    st.subheader("🎯 Segmentasi Demand")

    fig, ax = plt.subplots()
    sns.countplot(x='demand_cluster', data=filtered_df, ax=ax)
    st.pyplot(fig)

# ========================
# OPTIONAL: TEMP CATEGORY
# ========================
if 'temp_category' in filtered_df.columns:
    st.subheader("🌡️ Penyewaan Berdasarkan Kategori Suhu")

    fig, ax = plt.subplots()
    sns.boxplot(x='temp_category', y='cnt', data=filtered_df, ax=ax)
    st.pyplot(fig)

# ========================
# INFO DATASET
# ========================
st.sidebar.markdown("### 📌 Info Dataset")
st.sidebar.write(f"Jumlah data: {len(df)}")
st.sidebar.write("Periode: 2011–2012")

# ========================
# VALIDASI DATA
# ========================
if df.isnull().sum().sum() > 0:
    st.warning("⚠️ Terdapat missing values pada dataset!")

# ========================
# INSIGHT SINGKAT
# ========================
st.subheader("💡 Insight")

st.info("""
- Penyewaan meningkat pada suhu yang lebih tinggi  
- Cuaca buruk menurunkan jumlah penyewaan  
- Terdapat pola musiman dalam penggunaan sepeda  
""")