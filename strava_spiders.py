
import scrapy
# def authentication_failed(response):
#     # TODO: Check the contents of the response and return True if it failed
#     # or False if it succeeded.
#     pass

class ShareSpider(scrapy.Spider):
    name = "sharespider"
    start_urls = ['https://www.strava.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@id="login"]',
            formdata={
                'email': 'lkhain@yahoo.com',
                'password': 'Pingu2002',
                'Action':'1',
            },
            callback=self.parse
        )
    def parse(self, response):
        # if authentication_failed(response):
        #     self.logger.error("Login failed")
        #     return
        top_ten_page = response.url + '/segments/leader\?top_tens=true'  
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
    # def after_login(self, response):
    #     baseurl = 'http://www.example.com/public/'
    #     #Specify pages to crawl here:
    #     pagelist = ['page1.aspx', 'page2.aspx', 'page3.aspx', 'page4.aspx']
    #     for page in pagelist:
    #         yield scrapy.Request(url= baseurl + page + "?id=1",
    #         callback=self.action)

    # def action(self, response):
    #     pageurl = str(response.url)
    #     page = re.search('public/(.*)id=1', pageurl)
    #     if page:
    #         pagename = page.group(1)
    #     #Get page <title> element and strip whitespace
    #     title = str(response.selector.xpath('//title/text()').extract_first())
    #     res = title.strip()

    #     item = PageItem()
    #     item['pagename'] = pagename
    #     item['description'] = res
    #     yield item

# class StravaSpider(scrapy.Spider):

#     name = 'strava_spiders'
#     athlete = 16735685
#     start_url = [f'https://www.strava.com/athletes/{athlete}']


#     def parse(self, response):
#         top_ten_page = response.url + '/segments/leader?top_tens=true'  
#         yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)

#     def parse_top_tens(self, response):

#         top_tens = response.css('div.tab-content: a::attr(href)').getall()

#         for top_ten in top_tens:
#             yield scrapy.Request(url=top_ten, callback=self.parse_leaderboard)

#     def parse_leaderbord(self, response):
#         athlete_pages = response.css('td.athlete.track-click a::attr(href)').getall()
#         athlete = 16735685
#         target_account = f'/athletes/{athlete}'

#         for athletes in athlete_pages:
#             if(athletes != target_account):
#                 yield {"Strava Page": athlete}
#             else:
#                 break



