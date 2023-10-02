# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

#Gaya Latar Belakang
sns.set(style='white')

#Fungsi untuk membuat kerangka data sewa seiring waktu
def create_rents_over_time(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    monthly_df = df.resample('M', on='dteday').sum()
    return monthly_df

#Fungsi untuk menggabungkan persewaan sepeda berdasarkan kerangka data musim
def by_season(df):
    season_agg = df.groupby("season_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return season_agg

#Fungsi untuk menggabungkan persewaan sepeda berdasarkan kerangka data bulan
def by_month(df):
    monthly_agg = df.groupby("mnth_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return monthly_agg

#Fungsi untuk menggabungkan persewaan sepeda berdasarkan kerangka data harian
def by_day(df):
    weekday_agg = df.groupby("weekday_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return weekday_agg

#Fungsi untuk menggabungkan persewaan sepeda berdasarkan kerangka data jam
def by_hour(df):
    hourly_agg = df.groupby("hr").agg({
        "instant_y": "nunique",
        "cnt_y": ["max", "min"]
    })
    return hourly_agg


#Load CSV files
main_df = pd.read_csv("main_data.csv")
datetime_columns = ["dteday"]
main_df.sort_values(by="dteday", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

#Streamlit Sidebar
with st.sidebar:
    # Add Header
    st.header("Dashboard Bike-Sharing",divider='rainbow')
    st.header("by Arvi Ramadhan")

#Create Dataframes
rents_over_time_df = create_rents_over_time(main_df)
byseason_df = by_season(main_df)
bymonth_df = by_month(main_df)
byday_df = by_day(main_df)
byhour_df = by_hour(main_df)

#Visualisasi Penyewaan Sepeda Seiring Waktu (Digabung Berdasarkan Bulan).
st.subheader("Penyewaan Sepeda Seiring Waktu")
plt.figure(figsize=(10, 6))
plt.plot(rents_over_time_df.index, rents_over_time_df['cnt_x'], color='#6499E9')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Seiring Waktu (Digabung Berdasarkan Bulan)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader('Penyewaan Sepeda Berdasarkan Musim')
plt.figure(figsize=(10, 6))
x = byseason_df.index
y_max = byseason_df[('cnt_x', 'max')]
y_min = byseason_df[('cnt_x', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='#6499E9')
plt.bar(x, y_min, label='Min Rentals', color='orange')
season_labels = ['Musim ke-1', 'Musim ke-2', 'Musim ke-3', 'Musim ke-4']
plt.xticks(x, season_labels)
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Maks dan Min berdasarkan Musim')
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Bulan
st.subheader("Penyewaan Sepeda Berdasarkan Bulan")
plt.figure(figsize=(10, 6))
x = bymonth_df.index
y_max = bymonth_df[('cnt_x', 'max')]
y_min = bymonth_df[('cnt_x', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='#6499E9')
plt.bar(x, y_min, label='Min Rentals', color='orange')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Maks dan Min per Bulan')
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
plt.xticks(x,month_labels)
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Hari
st.subheader('Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.figure(figsize=(10, 6))
x = byday_df.index
y_max = byday_df[('cnt_x', 'max')]
y_min = byday_df[('cnt_x', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='#6499E9')
plt.bar(x, y_min, label='Min Rentals', color='orange')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Maks dan Min pada Hari')
plt.xticks(rotation=0)
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Visualisasi Penyewaan Sepeda berdasarkan Jam
st.subheader('Penyewaan Sepeda Berdasarkan Jam')
plt.figure(figsize=(10, 6))
x = byhour_df.index
y_max = byhour_df[('cnt_y', 'max')]
y_min = byhour_df[('cnt_y', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='#6499E9')
plt.bar(x, y_min, label='Min Rentals', color='orange')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Maks dan Min per Jam')
hour_labels = [str(i) for i in x]
plt.xticks(x, hour_labels)
plt.legend()

for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)