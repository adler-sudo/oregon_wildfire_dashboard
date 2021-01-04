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


# TODO: move this to a different module
# TODO: reduce the day range to 7?
def fire_count(df, interest_date, day_range=7):
    """
    Parameters:
        df: dataframe of interest. dataframe comes from geo table in fire.db and must already be
            parsed for the area of interest
        interest_date: date to look forward from
        day_range: # of days to look forward

    returns a count of the number of fires looking forward a specified # of days from a specified date
    """
    fires = len(df.loc[(df.report_date > interest_date) & (df.report_date < interest_date + datetime.timedelta(day_range))])

    return fires


def location_weather_df(location, analysis_type):
    """
    Parameters:
        location: must be exact location from fire database
        analysis_type: weather analysis type of interest (ie. PRCP, SNOW, etc.)
    """
    weather_con = sqlite3.connect('weatherData.db')
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


# TODO: will be able to be smarter and consolidate the fire count and fire df dataframes
# TODO: move this to a different module
def location_fire_df(latitude, longitude):
    """
    returns dataframe of fires within 0.5 degrees of latitude and longitude
    """
    fire_con = sqlite3.connect('fire.db')

    # make this a count query in the future
    fire_query = 'SELECT * FROM geo WHERE latitude < ? + 0.5 AND latitude > ? - 0.5 AND longitude < ? + 0.5 AND longitude > ? - 0.5'

    fire_df = pd.read_sql(fire_query, con=fire_con, params=[latitude, latitude, longitude, longitude], parse_dates=['report_date'])

    return fire_df


