import scrapy
import selenium
from selenium import webdriver
from scrapy.http import FormRequest
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time



class StravaScraper(scrapy.Spider):
    name = "test"
    athlete = '16735685'
    segments =[]
    
    allowed_domains = ['strava.com']
    start_urls = ['https://www.strava.com/login']
    

    def __init__(self):
        self.date_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08',
                          'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        self.month_before = {'Jan':'12','Feb':'01','Mar':'02','Apr':'03','May':'04','Jun':'05','Jul':'06','Aug':'07',
                          'Sep':'08','Oct':'09','Nov':'10','Dec':'11'}


    def parse(self, response):
        token = response.xpath('//*[@name="csrf-token"]/@content').get()
        return FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': token,
                                            
                                            'email': 'sashaprs@gmail.com',
                                            'password': 'PIC16BProject',
                                        },
                                        #dont_filter=True,
                                        #eta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                        callback=self.parse_after_login)
    

    def parse_after_login(self, response):
        #Try except statement for if user has no top tens
        top_ten_page = f'https://www.strava.com/athletes/{self.athlete}/segments/leader?top_tens=true'
    
        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)

    def parse_top_tens(self, response):
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()
        self.segments.extend(top_tens)
        next_page = response.xpath('//li[@class="next_page"]/a[@rel="next"]/@href').get()
        if(next_page):
            next_page_url = 'https://www.strava.com' + next_page
        
            yield scrapy.Request(url=next_page_url, callback = self.parse_top_tens)
            
        for top_ten in self.segments:

            if '/segments/' in top_ten:
            # yield {"top ten": 'https://www.strava.com' + top_ten}
                top_ten = 'https://www.strava.com' + top_ten
                yield scrapy.Request(url=top_ten, callback = self.parse_leaderboard)
    
    def parse_leaderboard(self, response):
        self.counter +=1
        self.url_list = [] 
        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
        dates = response.css('a[href^="/segment_efforts/"]::text').getall()
        #This get month of acheivement, we want month before acheivement
        edited_dates = []
        # for d in dates:
        #     month = self.date_dict[d[:3]]
        #     year = d[-4:]
        #     edited_dates.append(year+month)

        #New code: Defined new dictionary that gives month before, if month before is december, also subtracts one from year.
        for d in dates:
            month = self.month_before[d[:3]]
            if month == "12":
                year = int(d[-4:])
                year = str(year-1)
            else:
                year = d[-4:]
            edited_dates.append(year+month)

        athlete = '16735685'  # Ensure this is a string

        athletes_data = {}  # Dictionary to store athlete URLs and corresponding dates

        for i, athlete_url in enumerate(athlete_pages):
            if athlete_url.endswith(f'/athletes/{athlete}'):
                break
            athlete_url = 'https://www.strava.com' + athlete_url
            athletes_data[athlete_url] = edited_dates[i]

        for athlete_url, date in athletes_data.items():
            interval = str(date)
        
            year_offset = str(2023 - int(year))
            athlete_url = f'{athlete_url}#interval?interval={interval}&interval_type=month&chart_type=miles&year_offset={year_offset}'
            yield {'Athlete': athlete_url}
                
            
