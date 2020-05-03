# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 00:44:53 2020

@author: james
"""

# import necessary modules
import pandas as pd
import plotly.express as px

# read in file
df = pd.read_csv('D:/fire_data/weather_data/01012017-06302017.csv')

# isolate the locations
dd = df.drop_duplicates(subset=['NAME'])
de = dd[['NAME', 'LATITUDE', 'LONGITUDE']]
de.reset_index(drop=True, inplace=True)

# sum the precipitation value
precip = df.groupby('NAME')['TMAX'].max()
mapper = {k: v for k, v in precip.items()}
de['precip'] = de.NAME.map(mapper)
de.dropna(subset=['precip'], inplace=True)
year = pd.to_datetime(df.DATE[1]).year

# plot
tt = px.scatter(de,
		x='LONGITUDE',
		y='LATITUDE',
		hover_data=['NAME', 'precip'],
		color = 'precip',
        size = de.precip.abs(),
		color_continuous_scale='reds',
		title='Oregon Precipitation Summary {}'.format(year))
tt.show()