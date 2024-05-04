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
if len(sys.argv) != 5:
    print("Usage: python grab_bodyscore.py <username> <password> <start_date(YYYY-MM-DD)> <end_date(YYYY-MM-DD)>")
    sys.exit(1)

# Parse the command line arguments
d0 = sys.argv[3]
d1 = sys.argv[4]

username = sys.argv[1]
password = sys.argv[2]

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

plt.plot(DF['Date-time'],DF['Body Score'],color=(1.0, 0.4, 0.0),alpha=0.75,lw=4)
plt.xlabel('Date-time')
plt.ylabel('Body Score')
plt.gca().set_xticks(days)
plt.gca().set_xticklabels(days,fontsize=10,rotation=90)
simpleaxis(plt.gca())
plt.gca().set_facecolor('lightgray')
plt.subplots_adjust(bottom=0.2)
plt.savefig(f"./downloads/{username}_{d0}_{d1}.jpg")
DF[['Date-time','Body Score']].to_csv(f"./downloads/{username}_{d0}_{d1}.csv",index=True)
