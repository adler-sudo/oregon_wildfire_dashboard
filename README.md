# oregon_wildfire_dashboard
A dashboard for visualization of Oregon Wildfire Data from 1961-2019





All wildfire data collected from Oregon Wildfire Database
https://apps.odf.oregon.gov/divisions/protection/fire_protection/fires/firesreports.asp

All weather data collected from National Centers for Environmental Information
https://www.ncdc.noaa.gov/cdo-web/search;jsessionid=4D0E0D3F1AD03E1FCC55E67EAA0CE329


# Weather Download Instructions:
Use the selenium_weather.py script. There is a function there that can allow you to request all of the data for the specified values listed in the function. The documents will be emailed to you in csv format. From there, you can automate the download of the csv files from the emails and upload them to your own weather database. 
NOTE: The weather database has a limit to the number of Station Years you can download at one time. For Oregon, I was able to split the requests into 6 month increments to get all of the data that I was interested in.

# ML Implementation:
The first steps of the model implementation have been initiated. We use an xgboost regression model to predict # of fires that will occur within in area in the next 7 days given precipitation average over the last 7, 30, 60, 120, and 365 days. The model is currently very basic and we have not performed any hyperparameter tuning. We want to incorporate temperature and snow into the model going forward. More to come.

# Running the app
Run the app from the index.py file. This will provide links to each of the 6 applications.