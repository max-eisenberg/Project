import scrapy
from scrapy.http import FormRequest
from scrapy_selenium import SeleniumRequest


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

        self.url_list = []
    
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
        
        '''
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()
        for element in top_tens:
            segment = 'https://www.strava.com' + element
            if segment not in self.segments:
                if '/segments/' in segment:
                # self.segments.append(segment)
                    yield scrapy.Request(url=segment, callback=self.parse_leaderboard)

        next_page = response.xpath('//li[@class="next_page"]/a[@rel="next"]/@href').get()
        if next_page:
            next_page_url = 'http://strava.com' + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse_leaderboard )
        '''


    def parse_leaderboard(self, response):
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
            year_offset = str(2023 - int(year))


        athlete = '16735685'  # Ensure this is a string

        athletes_data = {}  # Dictionary to store athlete URLs and corresponding dates

        for i, athlete_url in enumerate(athlete_pages):
            if athlete_url.endswith(f'/athletes/{athlete}'):
                break
            athlete_url = 'https://www.strava.com' + athlete_url
            athletes_data[athlete_url] = edited_dates[i]

        for athlete_url, date in athletes_data.items():
            interval = str(date)
        

            athlete_url = f'{athlete_url}#interval?interval={interval}&interval_type=month&chart_type=miles&year_offset={year_offset}'
            # yield {"Athlete page": athlete_url, "date": date} #276 athlete pages
            #yield scrapy.Request(url=athlete_url, callback=self.start_request)
            self.url_list.append(athlete_url)
        yield SeleniumRequest(callback = self.start_request)
    
    # def start_request(self):
    #     url = 'https://www.strava.com/login'
    #     yield SeleniumRequest(url=url, callback=self.log_in)
        
    # def log_in(self):
    #     username = self.driver.find_element_by_name("Your Email")
    #     password = self.driver.find_element_by_name("Password")
    #     username.send_keys("sashaprs@gmail.com")
    #     password.send_keys("PIC16BProject")
    #     self.driver.find_element_by_xpath("//input[@name='login-button']").click()
        

    def start_request(self):
        urls = ['https://www.strava.com/login']
        for url in urls:
            yield SeleniumRequest(
                url= url,
                callback=self.parse,
                wait_time=3)

    def parse(self,response):
        scrape_url = "http://www.example.com/authen_handler.aspx"
        driver.get(scrape_url)        
        username = self.driver.find_element_by_name("Your Email")
        password = self.driver.find_element_by_name("Password")
        username.send_keys("sashaprs@gmail.com")
        password.send_keys("PIC16BProject")
        self.driver.find_element_by_xpath("//input[@name='login-button']").click()



    def parse_activities(self, response):
        '''
        limited_data = response.css('.limited')
        if limited_data:
            return
        
        stats = response.css('ul.list-stats.preview-stats.bottomless li div.stat')

        for stat in stats:
            distance_unit = stat.css('span.stat-subtext.caption::text').get()
            distance = stat.css('b.stat-text.value::text').get()
            print(distance,distance_unit)

        yield {
            'Distance Unit': distance_unit.strip() if distance_unit else None,
            'Distance': distance.strip() if distance else None
        }
        
        '''
        
        activity_values = response.css('div.------packages-ui-Stat-Stat-module__statValue--phtGK').getall()
        activity_units = response.css('div.------packages-ui-Stat-Stat-module__statValue--phtGK abbr.unit::attr(title)').getall()
    
        for value, unit in zip(activity_values, activity_units):
            yield {
                "Activity Value": value.strip(),  # Remove leading/trailing spaces
                "Activity Unit": unit if unit else "No unit specified"  # Provide default message if unit is not found
            }
    
    '''

    
    
    def parse_activities(self, response):
        athlete_name = response.css('h1.text-title1.athlete-name::text').get()

        monthly_stats = response.css('ul#totals').getall()

        for monthly_data in monthly_stats:
            #this gets the data from the total table at the top using regular expressions
            stats = re.findall(r'<strong>([\d.]+)<abbr class="unit" title="([^"]+)">', monthly_data)
            
            # here im matching the data with the appropriate unit (mi, hour, ft)
            stats = [(match[0], match[1]) for match in stats]  
            
            #combine the all of the stats for a given athlete
            #messy but i couldnt figure out another way
            combined_entries = []
            for i in range(0, len(stats), 4): 
                if i + 3 < len(stats):  
                    combined_entry = (
                        stats[i][0] + " " + stats[i][1],  # Combine elements from indices i and i+1
                        stats[i+1][0] + ":" + stats[i+2][0] + " " + stats[i+2][1] + "s",  # Combine elements from indices i+1, i+2, and i+2
                        stats[i+3][0] + " " + stats[i+3][1]  # Combine elements from indices i+3 and i+3
                    )
                    combined_entries.append(combined_entry)

            for elements in combined_entries:
                yield {"Athlete Name": athlete_name, "Monthly Stats": elements}
                
        '''