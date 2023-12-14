import scrapy
from scrapy.http import FormRequest


class StravaScraper(scrapy.Spider):
    name = "test"
    athlete = '16735685'
    segments =[]
    def __init__(self):
        self.date_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08',
                          'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    
     
    allowed_domains = ['strava.com']
    start_urls = ['https://www.strava.com/login']

    def parse(self, response):

        token = response.xpath('//*[@name="csrf-token"]/@content').get()
        return FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': token,
                                            
                                            'email': 'vandaelenmieke@gmail.com',
                                            'password': 'Pic16Bproj!',
                                        },
                                        #dont_filter=True,
                                        #eta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                        callback=self.parse_after_login)


    def parse_after_login(self, response):
        #Try except statement for if user has no top tens
        top_ten_page = f'https://www.strava.com/athletes/{self.athlete}/segments/leader?top_tens=true'
    
        yield scrapy.Request(url=top_ten_page, callback=self.parse_leaderboard)

    def parse_leaderboard(self, response):
        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
        dates = response.css('a[href^="/segment_efforts/"]::text').getall()
        yield{"Dates":dates}
        edited_dates = []
        for d in dates:
            month = self.date_dict[d[:3]]
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
            # yield {"Athlete page": athlete_url}
            yield scrapy.Request(url=athlete_url, callback=self.parse_activities)

    def parse_activities(self, response):
        if response.css('.limited'):
            #User is private
            return