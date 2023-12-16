import scrapy
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

activities = pd.DataFrame()
#Testing links
test = ['https://www.strava.com/athletes/29127886#interval_type?chart_type=miles&interval_type=month&interval=202012&year_offset=3','https://www.strava.com/athletes/5838343#interval_type?chart_type=miles&interval_type=month&interval=201803&year_offset=5','https://www.strava.com/athletes/28626466#interval_type?chart_type=miles&interval_type=month&interval=202205&year_offset=1']

#Actual data,, Set up chrome driver for selenium
urls = pd.read_csv('Interval_pages.csv')
urls_list = urls['Athlete page']
executable_path="/Users/sasha/Documents/PIC16B/strava_scraper/strava_scraper/spiders/chromedriver"
driver = webdriver.Chrome(executable_path=executable_path)
        
#Login to strava
driver.get('https://www.strava.com/login')
email_field = driver.find_element_by_id('email')
email_field.send_keys('sashaprs@gmail.com')
password_field = driver.find_element_by_id('password')
password_field.send_keys('PIC16BProj')
login_button = driver.find_element_by_id('login-button')
login_button.click()

#Collect activity data
for url in urls_list:
    temp=[]
    activity_stats = [] 
    names = []
    driver.get(url)
    driver.implicitly_wait(10)
    #Only get data drom public profiles
    #Store name, distance, elevation, time
    try:
        athlete = driver.find_element(By.CSS_SELECTOR, "h1.text-title1.athlete-name").text
        name = driver.find_elements(By.XPATH("//a[@data-testid='owners-name'"))
        for i in name:
            names.append(i.text)
        activity_values = driver.find_elements(By.CLASS_NAME, "------packages-ui-Stat-Stat-module__statValue--phtGK")
        for i in activity_values:
            temp.append(i.text)
        distance = temp[::3]
        elevation = temp[1::3]
        time = temp[2::3]
        df = pd.DataFrame({'Athlete':athlete,'Name':names,'Distance': distance, 'Elevation': elevation, 'Time': time})
        activities = pd.concat([activities, df], axis=0)
    except:
        pass
activities.to_csv('individual_acitivities.csv', index=False)
