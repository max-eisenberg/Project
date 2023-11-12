# to run 
# scrapy crawl tmdb_spider -o movies.csv

# Add these lines in settings
# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# CLOSESPIDER_PAGECOUNT = 20
# # Obey robots.txt rules
# ROBOTSTXT_OBEY = False

import scrapy
# def authentication_failed(response):
#     # TODO: Check the contents of the response and return True if it failed
#     # or False if it succeeded.
#     pass

class ShareSpider(scrapy.Spider):
    name = "sharespider"
    start_urls = ['https://www.strava.com/login']
    athlete = '16735685'

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={ 
                'email': '',
                'password': '',
            },
            callback=self.after_login
        )
    def after_login(self, response):
        top_ten_page = f'https://www.strava.com/athletes/{self.athlete}/segments/leader?top_tens=true'
        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)

    # def parse(self, response):
    #     # if authentication_failed(response):
    #     #     self.logger.error("Login failed")
    #     #     return
    #     top_ten_page = response.url + f"/atheletes/{athlete}/segments/leader\?top_tens=tru"
    #     # top_ten_page = 'https://www.strava.com/athletes/16735685/segments/leader?top_tens=true'
    #     # top_ten_page = response.url + '/segments/leader\?top_tens=true'  
    #     yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)


    def parse_top_tens(self, response):
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()
        # top_tens = response.css('div.tab-content: a::attr(href)').getall()
        for top_ten in top_tens:
            if '/segments/' in top_ten:
                # yield {"top ten": 'https://www.strava.com' + top_ten}
                top_ten = 'https://www.strava.com' + top_ten
                yield scrapy.Request(url=top_ten, callback=self.parse_leaderboard)


    def parse_leaderboard(self, response):
        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
        # date = response.css('div#results tbody tr td.track-click:nth-child(3) a::text').getall()

        athlete = 16735685
        target_account = f'/athletes/{athlete}'


        for athletes in athlete_pages:
            
            if(athletes == target_account):
                break
            athletes = 'https://www.strava.com' + athletes
            yield {"Strava Page": athletes}
            # yield {"Strava Page": athletes, "Date of Achievement": date}









