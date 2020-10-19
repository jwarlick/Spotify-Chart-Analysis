'''
SPOTIFYTRACK.py
Written by John Warlick in late 2019

A script to scrape Spotify public data to CSV and SQL databases.
Uses BeautifulSoup, SQLAlchemy, and requests libraries.
Certainly not the most efficient scraper for performing this function, but still functional.

Based on a [now-deleted] Spotify scraper built by Reddit user 'mbizkid', originally found below:
https://www.reddit.com/r/learnpython/comments/becnzn/i_built_a_web_scraper_for_spotify_top_200_daily/

DISCLAIMERS:
Having written this _as_ I was learning Python, it is clunky and quite inefficient.
This script in particular is problematic because it was designed to be run only once. 
Removing all SQL functionality - lines 31-62 & 127-165 - would make this script much faster.
I hope to find time to update this incorporating what I've learned at UCLA's MSBA program before the end of the year!

'''

# creates Spotify.com chart scraper
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from time import time
from time import sleep
from random import randint
import pandas as pd
import csv

# Imports SQLAlchemy and creates a supplementary SQL database in the working directory
from sqlalchemy import Column, ForeignKey, Integer, String, MetaData
from sqlalchemy import create_engine
engine = create_engine('sqlite:///spotifytrack.db', echo=None) 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship


# Creates the SQL Table Artist
class Artist(Base):
    __tablename__ = 'artists'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)

# Creates the SQL Table Song: tracks performance of singles in Top 200
class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key = True)
    songname = Column(String)
    daily_streams = Column(Integer)
    peak_streams = Column(Integer)
    cum_streams = Column(Integer)
    daily_chart = Column(Integer)
    highest_chart = Column(Integer)
    peak_date = Column(String)
    art_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates = "songs")

# Sets relationship between SQL Tables
Artist.songs = relationship("Song", order_by = Song.id, back_populates = "artist")
Base.metadata.create_all(engine)

# Checks for master CSV data output, and creates CSV with appropriate heading if nonexistent
with open("MasterSpotifyData.csv", mode="a", newline="") as f:
    data_handler = csv.writer(f, delimiter=",")
    row_count = 0
    for row in open("MasterSpotifyData.csv"):
        row_count += 1
    if row_count == 0:
        data_handler.writerow(["SongTitle", "Artist", "DailyStreams", "ChartRank", "Date", "DayOfWeek"])

# Sets base Spotify.com URL
base_url = 'https://spotifycharts.com/regional/global/daily/'

# Sets scraping date range
start = date(2020, 1, 1)
end = date.today()
iter = timedelta(days=1)
start_time = time()
mydate = start

# Creates empty array to hold all potentially scraped data
all_rows = []

while mydate < end:

    while mydate in skip:
        mydate += iter

    if(mydate > end):
        break

    # Connects to Spotify.com charts at specific page for each date 
    data = requests.get(base_url + mydate.strftime('%Y-%m-%d'))
    mydate += iter

    # Suspends script before each day's go-around to be generous with processing power
    sleep(randint(1,3))

    # Creates BeautifulSoup HTML parser
    soup = BeautifulSoup(data.text, 'html.parser')

    # Establishes where data we are interested starts and ends
    chart = soup.find('table', {'class': 'chart-table'})
    tbody = chart.find('tbody')

    # Scrapes data!
    for tr in tbody.find_all('tr'):

        # Scrapes each chart position
        rank_text = tr.find('td', {'class': 'chart-table-position'}).text

        # Scrapes artist name, removes unnecessary language
        artist_text = tr.find('td', {'class': 'chart-table-track'}).find('span').text
        artist_text = artist_text.replace('by ','').strip()

        # Scrapes song title
        title_text = tr.find('td', {'class': 'chart-table-track'}).find('strong').text

        # Scrapes daily streams
        streams_text = tr.find('td', {'class': 'chart-table-streams'}).text

        # Corrects date
        date = (mydate - iter)

        # Adds artist-specific data to Artist SQL table
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind = engine)
        session = Session()
        result = session.query(Artist).all()
        charted_artists = [row.name for row in result]
        if artist_text not in charted_artists:
            a1 = Artist(name = artist_text)
            session.add(a1)
            session.commit()
        
        # Adds song-specific data to Song SQL table
        almoststreams = streams_text.replace(",","")
        streams = int(almoststreams)
        result = session.query(Song).all()
        charted_songs = [item.songname for item in result]
        if title_text in charted_songs:
            
            # Updates chart placement and streaming data for songs already in Song table
            s = session.query(Song).filter_by(songname=title_text)
            for row in s:
                if int(rank_text) < row.highest_chart:
                    x = session.query(Song).get(row.id)
                    x.highest_chart = int(rank_text)
                    x.peak_date = date.strftime('%Y-%m-%d')
                    session.commit()
                if streams > row.peak_streams:
                    x = session.query(Song).get(row.id)
                    x.peak_streams = streams
                    session.commit()
                row.daily_chart = int(rank_text)
                row.cum_streams = row.cum_streams + streams
                session.commit() 
        else:
            s = session.query(Artist).filter_by(name=artist_text)
            for row in s:
                s1 = Song(songname = title_text, daily_streams = streams, peak_streams = streams, cum_streams = streams, daily_chart = int(rank_text), highest_chart = int(rank_text), peak_date = date.strftime('%Y-%m-%d'), art_id = row.id)
            session.add(s1)
            session.commit()

        # Collects all scraped data to one line of array
        all_rows.append([title_text, artist_text, streams, int(rank_text), date.strftime('%Y-%m-%d'), date.strftime('%A')])

    
# Informs user in output that a date has been scraped
date_text = mydate.strftime('%Y-%m-%d')
print(f"{date_text} chart data scraped")

# Appends all scraped data to master CSV
with open("MasterSpotifyData.csv", "a") as f:
    data_handler = csv.writer(f, delimiter=",")
    data_handler.writerows(all_rows)