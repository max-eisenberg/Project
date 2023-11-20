#Keep parse function and after login function. make callback of after login funciton the one you want to test. then put function you want to test 

import scrapy
from scrapy.http import FormRequest


class StravaScraper(scrapy.Spider):
    name = "test"
    athlete = '16735685'
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
                                            
                                            'email': 'lkhain@yahoo.com',
                                            'password': 'Pingu2002',
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

        for top_ten in top_tens:

            if '/segments/' in top_ten:
                # yield {"top ten": 'https://www.strava.com' + top_ten}
                top_ten = 'https://www.strava.com' + top_ten
                
                #what if we instead just pass the activity that corresponds to that best spot 
                yield{"top tens":top_ten}
                # yield scrapy.Request(url=top_ten, callback=self.parse_leaderboard)



