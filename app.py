import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("📊 HR Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("HR_Analytics.csv")

df = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Filter Departemen
departments = df['Department'].unique()
selected_dept = st.sidebar.selectbox("Pilih Departemen", options=["Semua"] + list(departments))

# Filter Usia
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
selected_age_range = st.sidebar.slider("Rentang Usia", min_age, max_age, (min_age, max_age))

# Filter Jenis Kelamin
gender_options = ["Semua"] + list(df['Gender'].unique())
selected_gender = st.sidebar.selectbox("Jenis Kelamin", options=gender_options)

# Filter Level Jabatan
job_levels = ["Semua"] + sorted(list(df['JobLevel'].unique()))
selected_job_level = st.sidebar.selectbox("Level Jabatan", options=job_levels)

# Terapkan filter
if selected_dept != "Semua":
    df = df[df['Department'] == selected_dept]
if selected_gender != "Semua":
    df = df[df['Gender'] == selected_gender]
if selected_job_level != "Semua":
    df = df[df['JobLevel'] == int(selected_job_level)]
df = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1])]

# KPI Cards
st.subheader("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    attrition_rate = (df['Attrition'].value_counts(normalize=True) * 100).get('Yes', 0)
    st.metric("Tingkat Attrition", f"{attrition_rate:.1f}%")

with col2:
    avg_income = df['MonthlyIncome'].mean()
    st.metric("Rata-rata Gaji Bulanan", f"Rp {avg_income:,.0f}")

with col3:
    avg_satisfaction = df['JobSatisfaction'].mean()
    st.metric("Rata-rata Kepuasan Kerja", f"{avg_satisfaction:.1f}/5")

with col4:
    avg_years = df['YearsAtCompany'].mean()
    st.metric("Rata-rata Lama Bekerja", f"{avg_years:.1f} Tahun")

# Visualisasi
st.subheader("📊 Analisis Visual")

# Baris 1: Attrition dan Distribusi Usia
col1, col2 = st.columns(2)

with col1:
    st.write("Persentase Attrition")
    attrition_counts = df['Attrition'].value_counts()
    st.bar_chart(attrition_counts)

with col2:
    st.write("Distribusi Usia vs Attrition")
    age_attrition = df.groupby(['Age', 'Attrition']).size().unstack()
    st.bar_chart(age_attrition)

# Baris 2: Kepuasan Kerja dan Gaji
col3, col4 = st.columns(2)

with col3:
    st.write("Kepuasan Kerja per Departemen")
    dept_satisfaction = df.groupby('Department')['JobSatisfaction'].mean()
    st.bar_chart(dept_satisfaction)

with col4:
    st.write("Distribusi Gaji per Level Jabatan")
    job_income = df.groupby('JobLevel')['MonthlyIncome'].mean()
    st.bar_chart(job_income)

# Baris 3: Heatmap Korelasi
st.subheader("🔥 Analisis Korelasi")
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation = df[numeric_cols].corr()
st.write("Korelasi antar Variabel Numerik")
st.dataframe(correlation.round(2))

# Tambahkan penjelasan korelasi
st.write("""
Interpretasi Korelasi:
- Nilai mendekati 1: Korelasi positif kuat
- Nilai mendekati -1: Korelasi negatif kuat
- Nilai mendekati 0: Tidak ada korelasi
""")

# Analisis Statistik
st.subheader("📊 Analisis Statistik")

# Analisis berdasarkan Departemen
st.write("Analisis berdasarkan Departemen")
dept_analysis = df.groupby('Department').agg({
    'Attrition': lambda x: (x == 'Yes').mean() * 100,
    'MonthlyIncome': 'mean',
    'JobSatisfaction': 'mean',
    'YearsAtCompany': 'mean'
}).round(2)

st.write("Statistik per Departemen:")
st.dataframe(dept_analysis)

# Analisis berdasarkan Level Jabatan
st.write("Analisis berdasarkan Level Jabatan")
job_level_analysis = df.groupby('JobLevel').agg({
    'Attrition': lambda x: (x == 'Yes').mean() * 100,
    'MonthlyIncome': 'mean',
    'JobSatisfaction': 'mean',
    'YearsAtCompany': 'mean'
}).round(2)

st.write("Statistik per Level Jabatan:")
st.dataframe(job_level_analysis)

# Penjelasan Dashboard
with st.expander("ℹ️ Penjelasan Dashboard"):
    st.markdown("""
    NAMA ANGOTA KELOMPOK :
    - KUMARA FAWWAS ABHISTA (2200016100)
    - DIANRA AULISYAH TANJUNG (2200016093)
    
    Dashboard ini dirancang untuk membantu manajemen dan HR dalam mengambil keputusan strategis terkait pengelolaan karyawan dan peningkatan kinerja organisasi. Berikut penjelasan fungsi masing-masing bagian dashboard:

    - **Filter Data (Sidebar):**  
      Pengguna dapat menganalisis pada departemen, usia, jenis kelamin, dan level jabatan tertentu. Dengan filter ini, manajemen dapat mengidentifikasi masalah atau peluang spesifik pada kelompok karyawan tertentu. Filter ini memungkinkan analisis yang lebih fokus dan mendalam untuk setiap segmen karyawan.

    - **KPI Cards:**  
      Menampilkan indikator kunci yang penting untuk monitoring kesehatan organisasi:
      - Tingkat Attrition: Persentase karyawan yang keluar dari perusahaan
      - Rata-rata Gaji Bulanan: Indikator kompensasi dan struktur gaji
      - Rata-rata Kepuasan Kerja: Ukuran kepuasan karyawan (skala 1-5)
      - Rata-rata Lama Bekerja: Indikator retensi dan loyalitas karyawan

    - **Visualisasi Attrition & Distribusi Usia:**  
      Menampilkan dua visualisasi penting:
      - Persentase Attrition: Menunjukkan proporsi karyawan yang keluar vs tetap
      - Distribusi Usia vs Attrition: Membantu mengidentifikasi kelompok usia yang paling rentan terhadap attrition

    - **Kepuasan Kerja & Distribusi Gaji:**  
      Menyajikan analisis komparatif:
      - Kepuasan Kerja per Departemen: Membandingkan tingkat kepuasan antar departemen
      - Distribusi Gaji per Level Jabatan: Menunjukkan struktur kompensasi berdasarkan level jabatan

    - **Analisis Korelasi:**  
      Menampilkan matriks korelasi antar variabel numerik yang membantu mengidentifikasi:
      - Hubungan antara variabel-variabel penting
      - Faktor-faktor yang saling terkait
      - Pola dan tren dalam data karyawan

    - **Analisis Statistik:**  
      Menyajikan analisis mendalam berdasarkan:
      - Departemen: Menampilkan statistik attrition, gaji, kepuasan kerja, dan lama bekerja per departemen
      - Level Jabatan: Menunjukkan perbandingan metrik penting antar level jabatan
      
      Analisis ini membantu manajemen dalam:
      - Mengidentifikasi departemen dengan masalah attrition tinggi
      - Mengevaluasi struktur kompensasi
      - Merancang program retensi yang tepat sasaran
      - Mengoptimalkan alokasi sumber daya

    Dashboard ini dirancang untuk mendukung pengambilan keputusan berbasis data dalam:
    1. Perencanaan SDM
    2. Pengembangan program retensi
    3. Evaluasi kebijakan kompensasi
    4. Identifikasi area yang memerlukan perhatian khusus
    5. Pengukuran efektivitas program HR
    """)

