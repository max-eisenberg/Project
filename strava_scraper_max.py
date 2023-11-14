import scrapy
from scrapy.http import FormRequest

class StravaScraper(scrapy.Spider):
    name = "strava_scraper"
    athlete = '16735685'

    allowed_domains = ['strava.com']
    start_urls = ['https://www.strava.com/login']


    def parse(self, response):
        token = response.xpath('//*[@name="csrf-token"]/@content').get()
        return FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token': token,
                                            
                                            'email': 'lkhain@yahoo.com',
                                            'password': 'Pingu2002'},
                                        #dont_filter=True,
                                        #meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                        callback=self.parse_after_login)


    def parse_after_login(self, response):

        top_ten_page = f'https://www.strava.com/athletes/{self.athlete}/segments/leader?top_tens=true'
    
        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)



    def parse_top_tens(self, response):
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()

        
        # What if we find the best result and only use that segment? 
        #best_spot = 0
        #best_activity = 'activity'
        #for top_ten in top_tens:
            #spot = response.css('div.text-title1::text').re_first(r'\d+')
            #if spot < best_spot:
                #best_spot = spot
                #best_activity = top_ten


        for top_ten in top_tens:

            if '/segments/' in top_ten:
                # yield {"top ten": 'https://www.strava.com' + top_ten}
                top_ten = 'https://www.strava.com' + top_ten
                
                #what if we instead just pass the activity that corresponds to that best spot 
                
                yield scrapy.Request(url=top_ten, callback=self.parse_leaderboard)


    def parse_leaderboard(self, response):
        
        

        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
        date = response.css('a[href^="/segment_efforts/"]::text').get()

        athlete = 16735685
        target_account = f'/athletes/{athlete}'


        for athletes in athlete_pages:
            
            if(athletes == target_account):
                break
            athletes = 'https://www.strava.com' + athletes
            yield {"Strava Page": athletes, "Date of Achievement": date}

