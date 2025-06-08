import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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
    fig1 = px.pie(df, names='Attrition', title='Persentase Attrition', 
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(df, x='Age', color='Attrition', 
                       title='Distribusi Usia vs Attrition',
                       barmode='group',
                       color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig2, use_container_width=True)

# Baris 2: Kepuasan Kerja dan Gaji
col3, col4 = st.columns(2)

with col3:
    fig3 = px.box(df, x='Department', y='JobSatisfaction', color='Attrition',
                  title='Kepuasan Kerja per Departemen',
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.box(df, x='JobLevel', y='MonthlyIncome', color='Attrition',
                  title='Distribusi Gaji per Level Jabatan',
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig4, use_container_width=True)

# Baris 3: Heatmap Korelasi
st.subheader("🔥 Analisis Korelasi")
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation = df[numeric_cols].corr()
fig5 = px.imshow(correlation,
                 title='Korelasi antar Variabel Numerik',
                 color_continuous_scale='RdBu')
st.plotly_chart(fig5, use_container_width=True)

# Analisis Prediktif
st.subheader("🔮 Analisis Prediktif Attrition")

# Persiapan data untuk model
le = LabelEncoder()
df_model = df.copy()
categorical_cols = ['Gender', 'Department', 'JobRole', 'MaritalStatus']
for col in categorical_cols:
    df_model[col] = le.fit_transform(df_model[col])

# Fitur untuk prediksi
features = ['Age', 'JobLevel', 'MonthlyIncome', 'JobSatisfaction', 
           'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion']
X = df_model[features]
y = df_model['Attrition'].map({'Yes': 1, 'No': 0})

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Tampilkan feature importance
feature_importance = pd.DataFrame({
    'Fitur': features,
    'Penting': model.feature_importances_
}).sort_values('Penting', ascending=False)

fig6 = px.bar(feature_importance, x='Fitur', y='Penting',
              title='Faktor-faktor yang Mempengaruhi Attrition',
              color='Penting',
              color_continuous_scale='Viridis')
st.plotly_chart(fig6, use_container_width=True)


# Penjelasan Dashboard
with st.expander("ℹ️ Penjelasan Dashboard"):
    st.markdown("""
    NAMA ANGOTA KELOMPOK :
    - KUMARA FAWWAS ABHISTA (2200016100)
    - DIANRA AULISYAH TANJUNG (2200016093)
    
    Dashboard ini dirancang untuk membantu manajemen dan HR dalam mengambil keputusan strategis terkait pengelolaan karyawan dan peningkatan kinerja organisasi. Berikut penjelasan fungsi masing-masing bagian dashboard:

    - **Filter Data (Sidebar):**  
      Pengguna dapat menganalisis pada departemen, usia, jenis kelamin, dan level jabatan tertentu. Dengan filter ini, manajemen dapat mengidentifikasi masalah atau peluang spesifik pada kelompok karyawan tertentu.

    - **KPI Cards:**  
      Menampilkan indikator kunci seperti tingkat attrition, rata-rata gaji bulanan, rata-rata kepuasan kerja, dan rata-rata lama bekerja. Informasi ini membantu manajemen memantau kesehatan organisasi secara umum dan mendeteksi area yang memerlukan perhatian khusus.

    - **Visualisasi Attrition & Distribusi Usia:**  
      Pie chart dan histogram memberikan gambaran cepat tentang proporsi karyawan yang keluar dan distribusi usia karyawan. Ini penting untuk memahami kelompok usia mana yang paling rentan terhadap attrition dan merancang program retensi yang tepat sasaran.

    - **Kepuasan Kerja & Distribusi Gaji:**  
      Box plot memperlihatkan variasi kepuasan kerja dan distribusi gaji di berbagai departemen dan level jabatan. Data ini membantu manajemen dalam mengevaluasi keadilan kompensasi dan efektivitas program peningkatan kepuasan kerja.

    - **Heatmap Korelasi:**  
      Menunjukkan hubungan antar variabel numerik, seperti hubungan antara lama bekerja, pendapatan, dan kepuasan kerja. Korelasi ini dapat digunakan untuk menemukan faktor-faktor yang paling berpengaruh terhadap attrition atau performa.

    - **Analisis Prediktif Attrition:**  
      Menggunakan model machine learning untuk mengidentifikasi faktor-faktor utama yang mempengaruhi kemungkinan karyawan keluar. Hasil ini dapat digunakan untuk merancang intervensi yang lebih efektif, seperti pelatihan, promosi, atau penyesuaian gaji.

    """)

