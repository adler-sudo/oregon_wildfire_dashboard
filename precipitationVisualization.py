# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 13:53:28 2020

@author: james
"""

#plotly visual of 2010 - 2020 precip by year by name

# import necessary modules
import pandas as pd
import plotly.express as px
import sqlalchemy

# connect to local weather database and pull data
engine = sqlalchemy.create_engine('sqlite:///weatherData.db')
conn = engine.connect()

query = 'SELECT observations.NAME, observations.PRCP, observations.DATE, locations.LATITUDE, locations.LONGITUDE FROM observations JOIN locations ON locations.NAME = observations.NAME'
results = conn.execute(query).fetchall()

df = pd.DataFrame(results)


# prep the first dataframe
df = pd.DataFrame(results,
                  columns=['NAME', 'PRCP', 'DATE', 'LATITUDE', 'LONGITUDE'])
df['YEAR'] = pd.to_datetime(df.DATE).dt.year
df.sort_values('DATE', inplace=True)
df.dropna(subset=['PRCP'], inplace=True)

# sum precipitation by year and name
precip = df.groupby(['YEAR', 'NAME'])['PRCP'].sum()

# prepare individual lists of items
# MAKE RELATIONAL DATABASE VALUES WITH LONGITUDES
# LATITUDES AND NAMES IN ORDER TO AVOID TAKING
# SO MANY OF THESE PREPATORY STEPS
mapper = {k:v for k, v in precip.items()}
years = [i[0] for i in mapper.keys()]
names = [i[1] for i in mapper.keys()]
precip = [mapper[k] for k in mapper.keys()]
latitudes = dict(zip(df.NAME, df.LATITUDE))
longitudes = dict(zip(df.NAME, df.LONGITUDE))

# prepare final dataframe for plotting
final = pd.DataFrame()
final['year'] = years
final['name'] = names
final['precip'] = precip
final['latitude'] = final.name.map(latitudes)
final['longitude'] = final.name.map(longitudes)

# plot the data
fig = px.scatter(final,
                 x='longitude',
                 y='latitude',
                 size='precip',
                 color='precip',
                 animation_frame='year')
fig.show()
