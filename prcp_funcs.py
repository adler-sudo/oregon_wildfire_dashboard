import datetime


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


def fire_count(df, interest_date, day_range=30):
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


