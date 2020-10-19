'''
SPOTWEEKTEST.py
Written by John Warlick in late 2019

To be used after SPOTIFYTRACKER.py and SPOTTOP200VISUALIZER.py as a bootstrap experiment for Spotify streaming data.

This is a bootstrap experiment I designed to test my suspicion that global top-200 Spotify plays increase linearly throughout the week.
It sums global streams for Spotify's Top 200 songs every day for the entire year, 
and then randomly shuffles each week's Mon/Tues/Wed/Thurs summed stream values with replacement into comparable "bootstrap weeks". 
The mean of the real weeks' slopes of summed global streams [from Mon->Thurs] is compared with that of the bootstrap weeks.
This process is repeated 100 times. 
The proportion of times the bootstrap weeks' mean streaming slope exceeded that of the real weeks is computed into a p value.

I have not tested this with 2020 data, but for 2019, I never obtained a p value exceeding .01.
The results held for a similar version of this script exploring the same relationship that disincluded Mondays.

I have hashed out the parts of this script that create the bootstrap weeks' "streaming" graphs. They are pretty, but cumbersome.

DISCLAIMERS:
Having written this _as_ I was learning Python, it is quite inefficient.
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
from bootstrapstats import draw_bs_pairs_linreg, ecdf

df = pd.read_csv('SpotifyTop200Streams.csv', names=['Date','Top200Streams','Day_Of_Week'])
df['Date'] = pd.to_datetime(df['Date'])

studystart = pd.to_datetime(date(2020, 1, 1))
studyend = pd.to_datetime(date(2020, 8, 13))
interdf = df.loc[df.Date <= studyend].copy()
weeksdf = interdf.loc[interdf.Date >= studystart].copy()
weeksdf['WeekNo'] = weeksdf.Date.dt.strftime('%W').copy()
weeksdf.WeekNo = weeksdf.WeekNo.astype('int64')

weeksdf = weeksdf[weeksdf.Day_Of_Week != "Friday"]
weeksdf = weeksdf[weeksdf.Day_Of_Week != "Saturday"]
weeksdf = weeksdf[weeksdf.Day_Of_Week != "Sunday"]

obs_slopes = np.empty(weeksdf['WeekNo'].max())
obs_intercepts = np.empty(weeksdf['WeekNo'].max())

x = [0, 1, 2, 3]

for i in range(weeksdf['WeekNo'].max()):
    y = [int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Monday')]['Top200Streams'].values), 
        int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Tuesday')]['Top200Streams'].values),
        int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Wednesday')]['Top200Streams'].values),
        int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Thursday')]['Top200Streams'].values)]
    a, b = np.polyfit(x, y, 1)
    obs_slopes[i] = a
    obs_intercepts[i] = b

obs_mean_slope = obs_slopes.mean()

print(obs_mean_slope)

x_obsmean, y_obsmean = ecdf(obs_slopes)
_ = plt.plot(x_obsmean, y_obsmean, marker='.', linestyle='none')
_ = plt.xlabel("Observed slope (plays per day)")
_ = plt.ylabel("ECDF")
plt.show()

bs_meanslope_reps = np.empty(100)

for q in range(100):
    bs_slopes = np.empty(weeksdf['WeekNo'].max())
    bs_intercepts = np.empty(weeksdf['WeekNo'].max())
    for i in range(weeksdf['WeekNo'].max()):
        y_np = [int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Monday')]['Top200Streams'].values), 
            int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Tuesday')]['Top200Streams'].values),
            int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Wednesday')]['Top200Streams'].values),
            int(weeksdf.loc[(weeksdf['WeekNo'] == (i + 1)) & (weeksdf['Day_Of_Week'] == 'Thursday')]['Top200Streams'].values)]
        y = np.array(y_np, dtype=int)
        x_array = np.array(x, dtype=int)
        inds = np.arange(len(x_array))
        bs_inds = np.random.choice(inds, size=len(inds), replace=True)
        bs_x = x_array
        bs_y = np.array([y[bs_inds][0], y[bs_inds][1], y[bs_inds][2], y[bs_inds][3]])
        c, d = np.polyfit(bs_x, bs_y, 1)  
        bs_slopes[i] = c
        bs_intercepts[i] = d
        
    bs_meanslope_reps[q] = bs_slopes.mean()

print(bs_meanslope_reps)
p = np.sum(bs_meanslope_reps >= obs_mean_slope) / 100
print('p = ', p)
x_bs_meanslope, y_bs_meanslope = ecdf(bs_meanslope_reps)

_ = plt.plot(x_bs_meanslope, y_bs_meanslope, marker='.', linestyle='none')
_ = plt.xlabel("Bootstrap mean slope (plays per day)")
_ = plt.ylabel("ECDF")

plt.show()
