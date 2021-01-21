import datetime
import sqlite3
import pandas as pd


def weather_average(df, interest_variable, interest_date, day_range=30):
    """
    Parameters:
        df: dataframe of interest
        interest_variable: weather variable of interest
        interest_date: date to look back from
        day_range: # of days to look back

    returns the average precipitation over a specified period of time looking back from a specified date
    """
    average = df.loc[(df.DATE > interest_date - datetime.timedelta(day_range)) & (df.DATE <= interest_date)][
        interest_variable].mean()

    return average


def location_weather_df(location, analysis_type, db_file='weatherData.db'):
    """
    Parameters:
        location: must be exact location from fire database
        analysis_type: weather analysis type of interest (ie. PRCP, SNOW, etc.)
    """
    weather_con = sqlite3.connect(db_file)
    columns = ['o.NAME', 'o.DATE', analysis_type, 'l.CITY', 'l.LATITUDE', 'l.LONGITUDE']
    weather_query = 'SELECT %s ' \
            'FROM observations AS o ' \
            'JOIN locations AS l ' \
            'ON o.NAME = l.CITY ' \
            'WHERE l.CITY = ?' % ','.join(columns)

    weather_df = pd.read_sql(weather_query, con=weather_con, params=[location], parse_dates=['DATE'])

    weather_df.sort_values('DATE', inplace=True)
    weather_df.reset_index(drop=True, inplace=True)

    return weather_df

