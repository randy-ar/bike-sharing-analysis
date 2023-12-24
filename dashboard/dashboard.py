import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from pathlib import Path

# Define a consistent color palette
colors = ['#4285F4', '#34A853', '#FBBC05', '#EA4335']

# Set Seaborn and Matplotlib style with larger font size
sns.set(style='whitegrid', palette=sns.color_palette(colors))
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['axes.labelsize'] = 30
plt.rcParams['axes.titlesize'] = 30

# Read data
data_day = pd.read_csv(str(Path(__file__).resolve().parent)+"/data_day.csv")
data_hour = pd.read_csv(str(Path(__file__).resolve().parent)+"/data_hour.csv")


# Streamlit layout
st.set_page_config(page_title='Bike Sharing Analysis', page_icon='🚴‍♂️', layout='wide')

st.header('Bike Sharing Analysis :sparkles:')

# Subheader for daily bike usage
st.subheader("1. Daily Bike Usage")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
daily_use = data_day.groupby(['workingday'])['cnt'].sum()
labels = ['Weekend', 'Weekday']

ax[0].pie(daily_use, textprops={'fontsize': 40}, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax[0].set_title('Bike Usage by Day')
ax[0].set_xlabel('')

# Plot histogram
daily_use_weekday = data_day.groupby('workingday')['cnt'].apply(list).reset_index(name='cnt_list')
ax[1].hist([daily_use_weekday['cnt_list'][0], daily_use_weekday['cnt_list'][1]], alpha=0.5, label=labels, color=colors[:2])
ax[1].patch.set_alpha(0)

# Add average lines
ax[1].axvline(np.mean(daily_use_weekday['cnt_list'][1]), color=colors[0], linestyle='dashed', linewidth=1, label='Weekday Avg')
ax[1].axvline(np.mean(daily_use_weekday['cnt_list'][0]), color=colors[1], linestyle='dashed', linewidth=1, label='Weekend Avg')

# Set labels and title
ax[1].set_xlabel('Bike Usage Count')
ax[1].set_ylabel('Frequency')
ax[1].set_title('Bike Usage Histogram by Weekday and Weekend')
ax[1].legend(labelcolor='black')

# Set transparent background
fig.patch.set_alpha(0.0)
fig.patch.set_alpha(0.0)

# Display plot
st.pyplot(fig)

# Subheader for hourly bike usage
st.subheader("2. Hourly Bike Usage")
fig, ax = plt.subplots(figsize=(35, 15))

# Plot bar chart for hourly usage
hourly_use = data_hour.groupby(['hr'])['cnt'].sum()
ax.bar(hourly_use.index, hourly_use.values, color=colors[2])

# Add labels and title
ax.set_xlabel('Hour')
ax.patch.set_alpha(0)
ax.set_ylabel('Count')
ax.set_title('Bike Usage by Hour')

# Set transparent background
fig.patch.set_alpha(0.0)

# Display plot
st.pyplot(fig)

# Subheader for bike usage per season
st.subheader("3. Bike Usage by Season and Weather")
fig, ax = plt.subplots(figsize=(35, 15))

weather_mapping = {1: 'Clear/Few clouds',
                   2: 'Mist/Cloudy',
                   3: 'Light Snow/Light Rain',
                   4: 'Heavy Rain/Ice Pallets'}

# Mengganti nilai weathersit dengan deskripsi yang sesuai
data_day_weathersit = data_day.copy()
data_day_weathersit['weathersit'] = data_day['weathersit'].map(weather_mapping)
# Membuat kolom baru berdasarkan weathersit
data_day['is_clear'] = (data_day['weathersit'] == 1).astype(int)
data_day['is_mist'] = (data_day['weathersit'] == 2).astype(int)
data_day['is_light_snow'] = (data_day['weathersit'] == 3).astype(int)
data_day['is_heavy_rain'] = (data_day['weathersit'] == 4).astype(int)


# Plot bar chart for bike usage by season and weather
ax = sns.barplot(x='season', y='cnt', hue='weathersit', data=data_day_weathersit, palette=sns.color_palette(colors[:4]))

# Set labels and title
ax.set_title('4. Bike Rental by Season and Weather')
ax.set_xlabel('Season')
ax.set_ylabel('Count')
ax.patch.set_alpha(0)
ax.legend(title='Weather Situation',labelcolor='black')

# Set transparent background
fig.patch.set_alpha(0.0)

# Display plot
st.pyplot(fig)

# Subheader for user type comparison
st.subheader("4. User Type Comparison")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Pie chart for user type distribution
sizes = [data_day['casual'].sum(), data_day['registered'].sum()]
labels = ['Casual', 'Registered']
ax[0].pie(sizes , textprops={'fontsize': 40}, labels=labels, autopct='%1.1f%%', startangle=100, colors=colors[:2])
ax[0].set_title('User Type Distribution')

# Histogram for user type comparison
ax[1].patch.set_alpha(0)
ax[1].hist(data_day['casual'], alpha=0.5, color=colors[0], label='Casual')
ax[1].hist(data_day['registered'], alpha=0.5, color=colors[1], label='Registered')
ax[1].set_xlabel('Bike Usage Count (cnt)')
ax[1].set_ylabel('Frequency')
ax[1].set_title('User Type Comparison')
ax[1].legend(title='User Type', loc='upper right',labelcolor='black')

# Set transparent background
fig.patch.set_alpha(0.0)
fig.patch.set_alpha(0.0)

# Display plot
st.pyplot(fig)
