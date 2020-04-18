# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:35:36 2020

@author: james
"""

# uses selenium to interact with the weather data page

# import the modules
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# establish weather scrape function
def weatherScrape(beginYear, beginMonth, endYear, endMonth, email, state):
    """sends csv, through email, of all EVAP, SNOW, PRCP, TMIN, TMAX, TAVG
    weather data from specified beginning to specified end
    
    beginYear: first year of desired data
    
    beginMonth: first month of desired data (will begin at day 1)
    
    endYear: last year of desired data
    
    endMonth: last month of desired data (will end at last day of month)
    
    email: destination email for csv
    
    state: the state to be analyzed
    """
    
    # for loop to run through each year
    for i in range(beginYear, endYear):
        # set driver and connect to weather url
        driver = webdriver.Chrome('C:/Users/james/chromedriver.exe')
        driver.get('https://www.ncdc.noaa.gov/cdo-web/search;jsessionid=4D0E0D3F1AD03E1FCC55E67EAA0CE329')
        
        # select the 'Daily Summaries' option
        selectedDataset = driver.find_element_by_id('selectedDataset')
        Select(selectedDataset).select_by_visible_text('Daily Summaries')
        
        # select the 'States' option
        selectedCategory = driver.find_element_by_id('selectedResultType')
        Select(selectedCategory).select_by_visible_text('States')
        
        # input "Oregon" as the state
        selectedState = driver.find_element_by_id('selectedSearchString')
        selectedState.send_keys("{}".format(state))
        
        # select date range (STILL NEEDS WORK! LOOK UP INTERACTING
        # WITH CALENDARS USING SELENIUM)
        
        driver.find_element_by_id("dateRangeContainer").click()
        
        # select year ( can probably simplify this. look at day)
        year = driver.find_element_by_xpath('//*[@id="dateRangeContainer"]/div/div/div/span/div/div/div/select[1]')
        Select(year).select_by_visible_text('{}'.format(i))
        
        # select month (can probably simplify this. look at day)
        month = driver.find_element_by_xpath('//*[@id="dateRangeContainer"]/div/div/div/span/div/div/div/select[2]')
        Select(month).select_by_visible_text('{}'.format(beginMonth))
        
        # select day
        driver.find_element_by_xpath("//*[@id='dateRangeContainer']/div[1]/div[1]/div[1]/span[1]/div[1]/table[1]/tbody[1]/tr[1]/td[@data-handler='selectDay'][1]").click()
        
        
        time.sleep(2)
        
        
        # select end year ( can probably simplify this. look at day)
        year = driver.find_element_by_xpath('//*[@id="dateRangeContainer"]/div/div/div[2]/span/div/div/div/select[1]')
        Select(year).select_by_visible_text('{}'.format(i))
        
        # select end month (can probably simplify this. look at day)
        month = driver.find_element_by_xpath('//*[@id="dateRangeContainer"]/div/div/div[2]/span/div/div/div/select[2]')
        Select(month).select_by_visible_text('{}'.format(endMonth))
        
        # select end day
        driver.find_elements_by_xpath("//*[@id='dateRangeContainer']/div[1]/div[1]/div[2]/span[1]/div[1]/table[1]/tbody[1]/tr/td[@data-handler='selectDay']")[-1].click()
        
        
        # apply the date selection
        driver.find_element_by_xpath("//*[@id='noaa-daterange-form']/button[1]").click()
        
        
        time.sleep(2)
        
        
        # submit
        driver.find_element_by_id('searchSubmit').click()
        
        time.sleep(2)
        
        # hit proper buttons, select csv format, and move through pages
        driver.find_element_by_xpath("//*[@title='Add to cart']").click()
        
        time.sleep(2)
        
        driver.find_element_by_id("widgetBodyInner").click()
        
        time.sleep(2)
        
        driver.find_element_by_id("GHCND_CUSTOM_CSV").click()
        
        time.sleep(2)
        
        driver.find_element_by_xpath("//*[@id='cartContinue']/button[1]").click()
        
        
        time.sleep(2)
        
        
        driver.find_element_by_id("GEOGRAPHIC_LOCATION").click()
        
        time.sleep(2)
        
        # expand all options
        driver.find_element_by_xpath("//*[@id='dataTypesContainer']/div[1]/a[1]").click()
        
        time.sleep(2)
        
        # select EVAP, PRCP, SNOW, TAVG, TMAX, and TMIN data options
        driver.find_element_by_xpath("//*[@value='EVAP']").click()
        driver.find_element_by_xpath("//*[@value='PRCP']").click()
        driver.find_element_by_xpath("//*[@value='SNOW']").click()
        driver.find_element_by_xpath("//*[@value='TAVG']").click()
        driver.find_element_by_xpath("//*[@value='TMAX']").click()
        driver.find_element_by_xpath("//*[@value='TMIN']").click()
        
        
        time.sleep(2)
        
        
        # continue to move through pages
        driver.find_element_by_id("buttonContinue").click()
        
        
        time.sleep(2)
        
        
        # input desired email recipient
        driver.find_element_by_id("email").send_keys("{}".format(email))
        driver.find_element_by_id("emailConfirmation").send_keys("{}".format(email))
        
        
        time.sleep(2)
        
        
        # submit and close
        driver.find_element_by_id("buttonSubmit").click()
        
        
        time.sleep(10)
        
        
        driver.close()
