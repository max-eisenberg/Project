import requests
import pandas as pd


!curl -X POST https://www.strava.com/oauth/token \
        -F client_id=116153 \
        -F client_secret=e70b47d6694329629317b81a561bec8ef3b3ab15 \
        -F code=f028be391d3dfd3a6a84bae35a8b60ba12181b2b \
        -F grant_type=authorization_code

activities_url = 'https://www.strava.com/api/v3/athlete/activities'

#The authorization below comes from generating an authorization code and then running a 
#command in the terminal to exhange that for an access code.

headers = {'Authorization': 'Bearer c2ed8d592c55d10d79ec8395c31295855e0b56cf'}

activities = []

page = 1
per_page = 100  

while True:
    params = {'page': page, 'per_page': per_page}
    response = requests.get(activities_url, headers=headers, params=params)
    page_activities = response.json()
    
    if not page_activities:
        break  
    activities.extend(page_activities)
    page += 1



df = pd.DataFrame(all_activities)

keep = ['name', 'distance', 'moving_time', 'total_elevation_gain', 
                   'average_heartrate', 'weighted_average_watts', 'start_date']
df = df[keep]
df['distance'] = round(df['distance'] * 0.000621371192,2)
df['total_elevation_gain'] = round(df['total_elevation_gain'] * 3.28084,2)
df['moving_time'] = round(df['moving_time']/3600,2)
df['start_date'] = df['start_date'].str.slice(0, 10)

df = df.rename(columns={'name' : 'Name', 'distance' : 'Distance (mi)', 'moving_time' : 'Moving Time (hr)', 'total_elevation_gain' : 'Elevation Gain (ft)', 
                   'average_heartrate' : 'Average Heartrate (bpm)', 'weighted_average_watts' : 'Average Power (w)', 'start_date': 'Date'})

df




Scraper: 

Class Strava Scraper: 
    Start Url = Athelete (user) Profile
    parse top 10 page:
        athlete_site + /segments/leader?top_tens=true
    parse top tens:
        Get links for each top 10 segment
        direct to each link
    parse better atheletes:
        Find position in top ten
        get link of athletes and date of top 10 acheivement
    Parse better athlete training data:
        On better athlete profile scrape activity data (distance and elevation?) for month leading up to when record was set
        save into datatable (for reccomendation system)


        Notes : What if athelte doesn't have top tens