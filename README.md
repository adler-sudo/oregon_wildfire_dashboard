# oregon_wildfire_dashboard
A dashboard for visualization of Oregon Wildfire Data from 1961-2019


Download the files and run:
python app.py


All wildfire data collected from Oregon Wildfire Database
https://apps.odf.oregon.gov/divisions/protection/fire_protection/fires/firesreports.asp

All weather data collected from National Centers for Environmental Information
https://www.ncdc.noaa.gov/cdo-web/search;jsessionid=4D0E0D3F1AD03E1FCC55E67EAA0CE329


# Weather Download Instructions:
Use the selenium_weather.py script. There is a function there that can allow you to request all of the data for the specified values listed in the function. The documents will be emailed to you in csv format. From there, you can automate the download of the csv files from the emails and upload them to your own weather database. 
NOTE: The weather database has a limit to the number of Station Years you can download at one time. For Oregon, I was able to split the requests into 6 month increments to get all of the data that I was interested in.

# Weather Visualization Instructions:
Use the precipitationVisualization.py, quick_visual.py, weatherDataEDA.py, and temperature_visual.py scripts to begin looking at some geospatial data for your location of interest. Check out some of the plots in the plotly_charts and eda_charts to get some inspiration.

# Running the app
There are currently three separate applications located within the oregon wildfire dashboard. One for weather visualization: weather.py, one for fire map visualization, scoped.py, and one for visualization of stacked bar info on wildfires by year: app.py.
Call python <desired app> from the command line, and the app will begin running in your browser using dash app services.
Don't forget to install the required packages from the requirements.txt file.