import sqlite3
import pandas as pd
import datetime


def fire_count(df, interest_date, day_range=7):
    """
    Parameters:
        df: dataframe of interest. dataframe comes from geo table in fire.db and must already be
            parsed for the area of interest
        interest_date: date to look forward from
        day_range: # of days into the future

    returns a count of the number of fires looking forward a specified # of days from a specified date
    """
    fires = len(df.loc[(df.report_date > interest_date) & (df.report_date < interest_date + datetime.timedelta(day_range))])

    return fires


# TODO: will be able to be smarter and consolidate the fire count and fire df dataframes
def location_fire_df(latitude, longitude, db_file='fire.db'):
    """
    Parameters:
        latitude (float): latitude of area of interest
        longitude (float): longitude of area of interest
        db_file: location of db file
    returns dataframe of fires within 0.5 degrees of latitude and longitude
    """
    fire_con = sqlite3.connect(db_file)

    # make this a count query in the future
    fire_query = 'SELECT * FROM geo WHERE latitude < ? + 0.5 AND latitude > ? - 0.5 AND longitude < ? + 0.5 AND longitude > ? - 0.5'

    fire_df = pd.read_sql(fire_query, con=fire_con, params=[latitude, latitude, longitude, longitude], parse_dates=['report_date'])

    return fire_df
