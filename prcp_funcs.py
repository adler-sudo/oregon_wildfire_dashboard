import datetime


def interest_range(df, interest_date, day_range=30):
    average = df.loc[(df.DATE > interest_date - datetime.timedelta(day_range)) & (df.DATE < interest_date)][
        'PRCP'].mean()
    return average