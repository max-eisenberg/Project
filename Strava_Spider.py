

# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):

    name = 'tmdb_spider'
    athlete = 16735685
    strava_page = [f'https://www.strava.com/athletes/{athlete}']


    def parse(self, response):


        top_ten_page = response.url + '/segments/leader?top_tens=true'  
        

        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)




    def parse_top_tens(self, response):


        top_tens = response.css('div.tab-content: a::attr(href)').getall()


        for top_ten in top_tens:
            yield scrapy.Request(url=top_ten, callback=self.parse_leaderboard)



    def parse_leaderbord(self, response):

        athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()

        athlete = 16735685
        target_account = f'/athletes/{athlete}'

        for athletes in athlete_pages:
            if(athletes != target_account):
                yield {"Strava Page": athlete}
            else:
                break


