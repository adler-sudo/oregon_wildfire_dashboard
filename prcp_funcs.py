import datetime


def precipitation_average(df, interest_date, day_range=30):
    """
    Parameters:
        df: dataframe of interest
        interest_date: date to look back from
        day_range: # of days to look back

    returns the average precipitation over a specified period of time looking back from a specified date
    """
    average = df.loc[(df.DATE > interest_date - datetime.timedelta(day_range)) & (df.DATE <= interest_date)]['PRCP'].mean()

    return average
