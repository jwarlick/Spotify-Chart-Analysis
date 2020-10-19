'''
SPOTANALYZER.py
Written by John Warlick in late 2019

To be used after SPOTIFYTRACKER.py for basic analysis of Spotify top 200 data.

Performs five basic functions, as selected by user:
1-- Plots a basic graph showing a song's global Spotify streaming performance over the year of 2020
2-- Same as above, but for two songs instead of one, for the purpose of visual comparison
3-- Takes a range of dates and outputs a list of most "dominant" songs on Spotify in that date range, as computed by chart rank
4-- Takes a range of dates and outputs a list of the highest-streaming songs on Spotify in that date range
5-- Takes a range of dates and outputs the 5 songs most consistently rising and falling in chart rank in that date range

Calendar widget TKCalendar is written by Juliette Monsel, Neal Probert and github user 'drepekh'.
Basis of my TKCalendar code is taken from its documentation below:
https://github.com/j4321/tkcalendar

DISCLAIMERS:
Having written these analyses _as_ I was learning Python, they are quite inefficient.
One major issue in these that I plan to fix before I get into everything else is that the song selection by user is case sensitive.
The 5th analysis option is particularly computationally expensive, and only questionably useful; I may replace it when I update this script.
I hope to find time before the end of the year to fully update these analyses; for now, they are at least usable.

''' 
from tkcalendar import Calendar, DateEntry
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from dateutil.parser import parse 
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import pandas as pd
import csv
import sys
from datetime import datetime
plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime
from dateutil.parser import parse

# Clears plot in case of repeat runs
plt.clf()

date_start = datetime.datetime
date_end = datetime.datetime


def startcalendar():
    # Creates calendar for user to select starting date for analysis

    def print_sel():
        global date_start 
        date_start = np.datetime64(cal.selection_get())
        top.destroy()

    top = tk.Toplevel(root)
    mindate = pd.Timestamp(year=2018, month=11, day=23)
    maxdate = pd.Timestamp(year=2020, month=10, day=1)

    cal = Calendar(top, font="Arial 14", selectmode='day', foreground='black', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red', showweeknumbers = False,
                   showothermonthdays = False,
                   cursor="hand1", year=2020, month=1, day=1, date_pattern='y-mm-dd')
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()

def endcalendar():
    # Creates calendar for user to select ending date for analysis
    
    import datetime
    from dateutil.parser import parse

    def print_sel():
        global date_end 
        date_end = np.datetime64(cal.selection_get())
        print(date_end)
        top.destroy()

    top = tk.Toplevel(root)
    mindate = pd.Timestamp(year=2020, month=1, day=1)
    maxdate = pd.Timestamp(year=2020, month=10, day=1)

    cal = Calendar(top, font="Arial 14", selectmode='day', foreground='black', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red', showweeknumbers = False,
                   showothermonthdays = False,
                   cursor="hand1", year=2020, month=1, day=1, date_pattern='y-mm-dd')
    
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()    

def closecalendar():
    # Closes calendar
    root.quit()

days = mdates.DayLocator()  
months = mdates.MonthLocator() 
count = 1

while count == 1:
    
    choice = int(input(
        "\nChoose an option from the following: \n"
        "Type 1 to graph Spotify worldwide streaming performance for a specific song in 2020 \n"
        "Type 2 to compare two songs' 2020 Global Spotify streaming graphs \n"
        "Type 3 to check Spotify chart dominance for a particular time period \n"
        "Type 4 to check the top-streaming songs on Spotify for a particular time period \n"
        "Type 5 to check the songs most consistently rising and falling in chart rank for a particular time period \n\n"
        "Type -1 to quit.\n\n"))

    # Clears plot if user chooses to do more than one analysis
    plt.clf()

    # Quits
    if choice == -1:
        count = 0

    if choice == 1:
        while True:
            try:
                df = pd.read_csv('MasterSpotifyData.csv')
                songname = input("What song would you like to see the 2020 stream performance graph of? \n")
                df = df[df.SongTitle == str(songname)]
                
                if len(df.index) == 0:
                    raise Exception("Data is empty")
                if len(df.index) == 1:
                    raise Exception("Not enough data!")
                df['Date'] = pd.to_datetime(df['Date'])
            
                fig, ax = plt.subplots()
                ax.plot(df.Date, df.DailyStreams)
                locator = mdates.DayLocator(interval=1)
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_minor_locator(locator)
                plt.xlabel("Date")
                plt.ylabel("Daily streams")
                plt.title(songname + " 2020 US Spotify streams")
                fig.autofmt_xdate()
                plt.show()
                break
            except Exception:
                print("that song isn't in our database... try a more popular one (or spell the song right!)")
                continue

    elif choice == 2:
        while True:
            try:
                dtypes = {'SongTitle': 'str', 'Artist': 'str', 'DailyStreams': 'int', 'ChartRank': 'int', 'Date': 'str', 'DayOfWeek': 'str'}
                parse_dates = ['Date', 'DayOfWeek']
                df = pd.read_csv('MasterSpotifyData.csv', dtype=dtypes, parse_dates=parse_dates)
                songname1 = input("What's the first song you would like to compare?\n")
                df1 = df[df.SongTitle == str(songname1)]
                if len(df1.index) == 0:
                    raise Exception("Data is empty")
                if len(df1.index) == 1:
                    raise Exception("Not enough data!")
                songname2 = input("What's the second song you would like to compare?\n")
                df2 = df[df.SongTitle == str(songname2)]
                if len(df2.index) == 0:
                    raise Exception("Data is empty")
                if len(df2.index) == 1:
                    raise Exception("Not enough data!")
       
                fig, ax = plt.subplots()
                ax.plot(df1.Date, df1.DailyStreams, label=songname1)
                ax.plot(df2.Date, df2.DailyStreams, label=songname2)
                locator = mdates.DayLocator(interval=1)
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_minor_locator(locator)
                plt.xlabel("Date")
                plt.ylabel("Daily streams")
                plt.legend(loc="upper right")
                plt.title(songname1 + " & " + songname2 + " compared 2020 US Spotify streams")
                fig.autofmt_xdate()
                plt.show()
                break
            except Exception:
                print("that song isn't in our database... try a more popular one (or spell the song right!)")
                continue

    elif choice == 3:
        dtypes = {'SongTitle': 'str', 'Artist': 'str', 'DailyStreams': 'int', 'ChartRank': 'int', 'Date': 'str', 'DayOfWeek': 'str'}
        parse_dates = ['Date', 'DayOfWeek']
        df = pd.read_csv('MasterSpotifyData.csv', dtype=dtypes, parse_dates=parse_dates)

        # Generates calendar for the user to select a date range. Same construction in analysis choices 4 and 5.
        print("\nPick a start and end date")
        root = tk.Tk()
        ttk.Button(root, text='Start date', command=startcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='End date', command=endcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='Click when done', command=root.quit).pack(padx=10, pady=10)
        root.mainloop()
        root.update()
        if date_start > date_end:
            raise Exception("your end date is not before the start date")
        SDRdf = df[['SongTitle','ChartRank','Date']]
        SDRdf_timeperiod = SDRdf.loc[(SDRdf['Date'] <= date_end) & (SDRdf['Date'] >= date_start)] 
        print("\nThe songs with the highest average global chart rank on Spotify for that time period were: \n")
        print(SDRdf_timeperiod.groupby('SongTitle')['ChartRank'].mean().sort_values().head(10))

    elif choice == 4:
        dtypes = {'SongTitle': 'str', 'Artist': 'str', 'DailyStreams': 'int', 'ChartRank': 'int', 'Date': 'str', 'DayOfWeek': 'str'}
        parse_dates = [4, 5]
        df = pd.read_csv('MasterSpotifyData.csv', dtype=dtypes, parse_dates=parse_dates)
        print("\nPick a start and end date")
        root = tk.Tk()
        ttk.Button(root, text='Start date', command=startcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='End date', command=endcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='Click when done', command=closecalendar).pack(padx=10, pady=10)
        root.mainloop()
        if date_start > date_end:
            raise Exception("your end date is not before the start date")
        date_start_str = str(date_start)
        date_end_str = str(date_end)
        SSRdf = df[['SongTitle','DailyStreams','Date']]
        SSRdf_selection = SSRdf.loc[(SSRdf['Date'] <= date_end) & (SSRdf['Date'] >= date_start)] 
        print("\nThe most-streamed songs on Spotify for the time period between " + date_start_str + " and " + date_end_str + " were: \n")
        print(SSRdf_selection.groupby('SongTitle')['DailyStreams'].sum().sort_values(ascending=False).head(10))

    # Takes user dates and runs a time-series regression of Daily Streams for every song appearing on Spotify's chart.
    # Outputs the songs on the chart with highest and lowest slopes, equating to the most consistently rising and most 
    # consistently falling songs in that time period. Very computationally expensive.
    elif choice == 5:
        dtypes = {'SongTitle': 'str', 'Artist': 'str', 'DailyStreams': 'int', 'ChartRank': 'int', 'Date': 'str', 'DayOfWeek': 'str'}
        parse_dates = ['Date', 'DayOfWeek']
        df = pd.read_csv('MasterSpotifyData.csv', dtype=dtypes, parse_dates=parse_dates)
        print("\nPick a start and end date")
        root = tk.Tk()
        ttk.Button(root, text='Start date', command=startcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='End date', command=endcalendar).pack(padx=10, pady=10)
        ttk.Button(root, text='Click when done', command=closecalendar).pack(padx=10, pady=10)
        root.mainloop()
        if date_start > date_end:
            raise Exception("your end date is not before the start date")
        SSRdf = df[['SongTitle','DailyStreams','Date']]
        SSR = SSRdf.loc[(SSRdf['Date'] <= date_end) & (SSRdf['Date'] >= date_start)] 
        SSR['SimpDate'] = 0
        date_start = date_start.astype(datetime.date)
        for i, date in enumerate(SSR.loc[:,'Date']):
            z = SSR[['Date']].iloc[i][0].date()
            delta = z - date_start
            simp = delta.days
            SSR.iloc[i, 3] = simp

        streamslope = np.empty(len(SSR.loc[SSR['Date'] == date_end]['SongTitle']))
        streamintercept = np.empty(len(SSR.loc[SSR['Date'] == date_end]['SongTitle']))
        streamnames = ["" for x in range(len(SSR.loc[SSR['Date'] == date_end]['SongTitle']))]

        for i, song in enumerate(SSR.loc[SSR['Date'] == date_end]['SongTitle']):
            a, b = np.polyfit(SSR.loc[SSR.SongTitle == song, 'SimpDate'], SSR.loc[SSR.SongTitle == song, 'DailyStreams'], 1)
            streamslope[i] = a
            streamintercept[i] = b
            streamnames[i] = song
        d = {'SongTitle':streamnames, 'StreamSlope':streamslope, 'StreamIntercept':streamintercept}
        StreamFits = pd.DataFrame(data=d)
        print("\nThe 5 most consistently rising and falling in chart rank on Spotify for the time period selected were: \n")
        print(StreamFits.groupby('StreamSlope')['SongTitle'].head(10))