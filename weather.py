from sqlalchemy import Table, MetaData, create_engine, select
import pandas as pd
from sqlalchemy.orm import sessionmaker





# convert fire database to dataframe
engine = create_engine('sqlite:///weatherData.db')
conn = engine.connect()
metadata = MetaData()

# select weather table
observations = select([Table('observations', metadata, autoload=True, autoload_with=engine)])
locations = select([Table('locations', metadata, autoload=True, autoload_with=engine)])
weatherQuery = observations.join(locations, observations.c.NAME == locations.c.name)
recordsGeo = conn.execute(weatherQuery).fetchall()

dfGeo = pd.DataFrame(recordsGeo, columns=weather.columns.keys())
dfGeo.drop(columns=['index'], inplace=True)
dfGeo.dropna(subset=['total_acres'], inplace=True)

# select locations table






@app.callback
# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

