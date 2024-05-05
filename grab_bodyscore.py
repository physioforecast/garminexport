#!/usr/bin/env python
# coding: utf-8

from datetime import timedelta
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.ion()

import sys
sys.path.append("./")
from garminexport.garminclient import GarminClient

def simpleaxis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)


# Check if the required arguments are provided
if len(sys.argv) != 6:
    print("Usage: python grab_bodyscore.py <username> <password> <start_date(YYYY-MM-DD)> <end_date(YYYY-MM-DD)> <download path>")
    sys.exit(1)

# Parse the command line arguments
d0 = sys.argv[3]
d1 = sys.argv[4]

username = sys.argv[1]
password = sys.argv[2]

download_path = sys.argv[5]

client = GarminClient(username,password)

client.connect()

# Generate a list of days
days = pd.date_range(start=d0, end=d1, freq='D')

# Convert the list of days to a format like "YYYY-MM-DD"
days = [day.strftime('%Y-%m-%d') for day in days]

DF_ = []

for day in days:
    response = client.session.get(f"https://connect.garmin.com/wellness-service/wellness/dailyStress/{day}")
    try:    
        X = json.loads(response.text)["bodyBatteryValuesArray"]
        X = pd.DataFrame(X, columns=['minutes', 'type', 'Body Score', 'version'])
        X['minutes'] = np.array([0] + list(np.diff(X['minutes'] / 1000))) / 60
        X['minutes'] = np.cumsum(X['minutes'])

        # Example start datetime
        start_datetime = pd.Timestamp(json.loads(response.text)["startTimestampLocal"])

        X['Date-time'] = start_datetime + pd.to_timedelta(X['minutes'], unit='m')
        DF_.append(X)
    except Exception as e:
        print(f"Failed to process {day}: {e}")

if not DF_:
    print("No data found.")
    sys.exit(1)

DF = pd.concat(DF_)
plt.figure(figsize=(10,5))
plt.plot(DF['Date-time'],DF['Body Score'],color=(1.0, 0.1, 0.0),alpha=0.75,lw=2)
plt.ylabel('Body Score')


d1 = pd.to_datetime(d1) + pd.DateOffset(days=1)

# Create a date range with 4-hour frequency for time ticks
x_time = pd.date_range(start=d0, end=d1, freq='4h')

# Create a date range with 1-day frequency for date ticks at 24h
x_date = pd.date_range(start=d0, end=d1, freq='1d')

# Plotting
ax = plt.gca()
# Set the primary x-axis (time)
ax.set_xticks(x_time)
ax.set_xticklabels([date.strftime('%H:%M') for date in x_time], fontsize=10, rotation=90)

for day in x_date:
    ax.axvline(day,color='black',linestyle='--')

# Add a secondary x-axis for dates
h = ax.secondary_xaxis('bottom')
h.set_xticks(x_date)
h.set_xticklabels([date.strftime('%Y-%m-%d') for date in x_date],fontsize=10, rotation=0)
h.spines['bottom'].set_position(('outward', 40))  # Adjust the position as needed

simpleaxis(plt.gca())
plt.gca().set_facecolor((0.91,0.91,0.91))
plt.ylim([0,100])
plt.grid(True,color='white')
plt.subplots_adjust(bottom=0.5)

plt.savefig(f"{download_path}/{username}_{d0}_{d1}.jpg",dpi=300)
DF[['Date-time','Body Score']].to_csv(f"{download_path}/{username}_{d0}_{d1}.csv",index=True)
