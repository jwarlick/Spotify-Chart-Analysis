# Spotify Chart Analysis
Python/SQL scripts for tracking and basic analysis of scraped Spotify.com chart data.

### Scripts

**SPOTIFYTRACK.py** uses BeautifulSoup and SQLAlchemy to scrape public global Spotify.com chart data and save it into CSV and SQL data sources.

**SPOTIFYANALYZER.py** is a script-based toolset for doing basic analysis of the data gleaned from SPOTIFYTRACK.py, such as time-series graphs of individual songs' streaming performance and computing the top-performing songs across a time period.

**SPOTTOP200VISUALIZER.py** outputs a basic time-series visualization of the daily sum of streams from all top 200 songs on Spotify.

**SPOTWEEKTEST.py** is a bootstrap experiment I designed to test whether the results of SPOTTOP200VISUALIZER.py made sense - a test of whether Spotify's total daily streams from Top 200 songs tend to consistently increase from Monday to Thursday in a given week.


#### DISCLAIMER:

Having written these scripts _as_ I was learning Python, they are mostly quite inefficient, clunky, and ugly. However, they do function.

I hope to find time to update these scripts before the end of the year, incorporating what I've self-learned since writing them as well as what I've been taught at UCLA's MSBA program, which I started in September 2020.

Thank you for checking out my work!

John Warlick
