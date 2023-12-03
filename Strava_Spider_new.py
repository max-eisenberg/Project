import scrapy
from scrapy.http import FormRequest
import re
import time

class StravaScraper(scrapy.Spider):
    name = "miekespider"
    athlete = '16735685'
    segments = []
    interval_urls = []
    athletes = []

    def __init__(self):
        self.date_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08',
                          'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        self.month_before = {'Jan':'12','Feb':'01','Mar':'02','Apr':'03','May':'04','Jun':'05','Jul':'06','Aug':'07',
                          'Sep':'08','Oct':'09','Nov':'10','Dec':'11'}
        self.url_list = []

    allowed_domains = ['strava.com']
    start_urls = ['https://www.strava.com/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf-token"]/@content').get()
        return FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': token,
                                            
                                            'email': 'vandaelenmieke@gmail.com',
                                            'password': 'Pic16Bproj!',},
                                        #dont_filter=True,
                                        #eta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                        callback=self.parse_after_login)


    def parse_after_login(self, response):
        #Try except statement for if user has no top tens
        top_ten_page = f'https://www.strava.com/athletes/{self.athlete}/segments/leader?top_tens=true'
    
        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)
    
    def check_uphill(self,response):
        segment_grade = response.css('.list-stats.inline-stats.stats-lg li:nth-child(3) .stat-text::text').get().strip()
        segment_grade = segment_grade[0]
        if segment_grade != '-':
            self.segments.append(response.url)

    # def parse_top_tens(self, response):
    #     top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()
    #     # scrapy.Request(url= top_tens, callback = self.check_uphill)
    #     self.segments.extend(top_tens)
    #     next_page = response.xpath('//li[@class="next_page"]/a[@rel="next"]/@href').get()
    #     if(next_page):
    #         next_page_url = 'https://www.strava.com' + next_page
        
    #         yield scrapy.Request(url=next_page_url, callback = self.parse_top_tens)


    def parse_top_tens(self, response):
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()

        for element in top_tens:
            segment = 'https://www.strava.com' + element
            if segment not in self.segments:
                if '/segments' in segment:
                    self.segments.append(segment)
                    # yield{"Segments": segment}  #43 top ten
                    yield scrapy.Request(url = segment, callback = self.parse_leaderboard)

        next_page = response.xpath('//li[@class="next_page"]/a[@rel="next"]/@href').get()
        if next_page:
            next_page_url = 'http://strava.com' + next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse_top_tens)


    def parse_leaderboard(self, response):
        # yield{"Segments":response.url} # USE FOR OCCURENCES
        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
        for link in athlete_pages:
            athlete_page = ('https://www.strava.com' + link)
            # yield {"Athlete page": athlete_pages}
            yield scrapy.Request(url = athlete_page, callback=self.parse_activities)

        # dates = response.css('a[href^="/segment_efforts/"]::text').getall()
        # #This get month of acheivement, we want month before acheivement
        # edited_dates = []

        # for d in dates:
        #     month = self.month_before[d[:3]]
        #     if month == "12":
        #         year = int(d[-4:])
        #         year = str(year-1)
        #     else:
        #         year = d[-4:]
        #     year_offset = str(2023 - int(year))
        #     edited_dates.append(str(year)+str(month)+str(year_offset))


        # athlete = '16735685'  # Ensure this is a string

        # athletes_data = {}  # Dictionary to store athlete URLs and corresponding dates

        # for i, athlete_url in enumerate(athlete_pages):
        #     if athlete_url.endswith(f'/athletes/{athlete}'):
        #         break
        #     athlete_url = 'https://www.strava.com' + athlete_url
        #     # yield{"Athlete Page": athlete_url}  # How i got data for arch nemesis
        #     athletes_data[athlete_url] = edited_dates[i]

        # for athlete_url, date in athletes_data.items():
        #     # interval = str(date)
        #     interval = str(date)[:6]
        #     year_offset = str(date)[6:]
        

        #     athlete_url = f'{athlete_url}#interval_type?chart_type=miles&interval_type=month&interval={interval}&year_offset={year_offset}'
        #     self.interval_urls.append(athlete_url)
        #     # athlete_url = f'{athlete_url}#interval?interval={interval}&interval_type=month&chart_type=miles&year_offset={year_offset}'
                
            
        #     # yield {"Athlete page": athlete_url} #276 athlete pages
        #     yield scrapy.Request(url=athlete_url, callback=self.parse_activities)
        # yield {"Athlete page": athlete_pages} #276 athlete pages

        # yield scrapy.Request(url = athlete_pages, callback=self.parse_activities)


            
    def parse_activities(self, response):
        # time.sleep(2)
        # yield{"URL": response.url}
        # time.sleep(3)
        athlete_name = response.css('h1.text-title1.athlete-name::text').get()
        month = response.css('h2#interval-value.text-callout.left::text').get()
        monthly_stats = response.css('ul#totals').getall()

        for data in monthly_stats:
            stats = re.findall(r'<strong>([\d.,]+)<abbr class="unit" title="([^"]+)">', data)
            distance = stats[0][0] #+ " " + stats[0][1]
            time_spent = stats[1][0] #+ " " + stats[1][1] + "s"
            elevation = stats[2][0] #+ " " + stats[2][1]

            yield {
            "Athlete Name": athlete_name,
            "Monthly Distance": distance,
            "Monthly Time": time_spent,
            "Monthly Elevation": elevation, 
            "Timeframe" : month,
            "Source": response.url
            }
        # athlete_name = response.css('div.avatar-athlete::attr(title)').get()
        # yield {"Name": athlete_name, "Athlete URL": response.url}
        # #Add if private account
        # activity_links = response.css('h3.------packages-feed-ui-src-components-ActivityEntryBody-ActivityEntryBody__activity-name--pT7HD a::attr(href)').getall()

        # yield{"activities": activity_links}
    
        # try:
        #     # name = response.css('.profile-heading .avatar-athlete::attr(title)').get()
        #     links = response.css('a::attr(href)').extract()
        #     for link in links:
        #         if  "/activities" in link:
        #             link = 'https://www.strava.com'+ link
        #             # yield { "Athlete": name, "Activity Links": link}
        #             yield scrapy.Request(url=link, callback=self.parse_stats)
        # except:
        #     pass


    # def parse_stats(self, response):
    #     name = response.css('h2.text-title3.text-book span.title a::text').get()
    #     dist = response.css('ul.inline-stats li strong::text').get()
    #     dist = float(dist)
    #     time = response.css('ul.inline-stats li:nth-child(2) strong::text').get()
    #     elev = response.css('ul.inline-stats li:nth-child(3) strong::text').get()
    #     elev = int(elev.translate(str.maketrans("", "", ",")))

    #     yield{"Athlete Name": name, "Distance": dist, "Time Elapsed": time, "Elevation": elev}

    