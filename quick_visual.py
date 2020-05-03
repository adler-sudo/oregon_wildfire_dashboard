"""quick visualization of precipitation throughout Oregon in the first half of
1962 using data collected from weather stations"""

# import necessary modules
import pandas as pd
import plotly.express as px

# read in file
df = pd.read_csv('D:/fire_data/weather_data/07012017-12312017.csv')

# isolate the locations
dd = df.drop_duplicates(subset=['NAME'])
de = dd[['NAME', 'LATITUDE', 'LONGITUDE']]
de.reset_index(drop=True, inplace=True)

# sum the precipitation value
precip = df.groupby('NAME')['PRCP'].sum()
mapper = {k: v for k, v in precip.items()}
de['precip'] = de.NAME.map(mapper)
year = pd.to_datetime(df.DATE[1]).year

# plot
tt = px.scatter(de,
		x='LONGITUDE',
		y='LATITUDE',
		hover_data=['NAME', 'precip'],
		color = 'precip',
		size = 'precip',
		color_continuous_scale='magma',
		title='Oregon Precipitation Summary {}'.format(year))
tt.show()