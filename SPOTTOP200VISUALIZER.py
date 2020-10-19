'''
SPOTTOP200VISUALIZER.py
Written by John Warlick in late 2019

To be used after SPOTIFYTRACKER.py to make a basic visualization of global top-200 Spotify streaming activity.

Graphs the sum of daily streams of Spotify's global top 200 songs against date.

DISCLAIMERS:
Having written this _as_ I was learning Python, it is quite inefficient, and not exactly pretty.
This script in particular is problematic because it was designed to be run only once.
I hope to find time to update this incorporating what I've learned at UCLA's MSBA program before the end of the year!

'''

from dateutil.parser import parse 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import seaborn as sns
import numpy as np
import pandas as pd
import csv
import sys
from datetime import datetime, timedelta, date

# ___HASH OUT LINES 30-53 AFTER FIRST RUN OF SCRIPT!___

days = mdates.DayLocator()  
months = mdates.MonthLocator() 

# Sets dates for Visualizer. Change dates as is appropriate or desired.
start_date = (pd.to_datetime('2020-01-01', format='%Y-%m-%d')).date()
end_date = (pd.to_datetime('2020-10-01', format='%Y-%m-%d')).date()
my_date = start_date 
date_data = []

# Reads scraped Spotify.com chart data from master CSV, and creates new CSV for visualization purposes.
for single_date in (start_date + timedelta(n) for n in range(int((end_date - start_date).days))):

    converted_date = (pd.to_datetime(single_date).date())
    
    daily200streams = 0
    day_of_week = converted_date.strftime('%A')
    with open ("MasterSpotifyData.csv", "r") as g:
        timestreamdata = csv.reader(g)
        for line in timestreamdata:
            if str(line[4]) == str(converted_date):
                daily200streams += int(line[2])
    with open ("SpotifyTop200Streams.csv", "a") as f:
        data_handler = csv.writer(f, delimiter=",")
        data_handler.writerow([converted_date, daily200streams, day_of_week])

# Visualizes scraped data.
df = pd.read_csv('SpotifyTop200Streams.csv', names=['Date','Top200Streams','Day'])
df['Date'] = pd.to_datetime(df['Date'])
fig, ax = plt.subplots()
ax.plot(df.Date, df.Top200Streams)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(days)
plt.xlabel("Date")
plt.ylabel("Top200Streams")
fig.autofmt_xdate()
plt.show()
