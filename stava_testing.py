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
    
        yield scrapy.Request(url=top_ten_page, callback=self.parse_top_tens)

    def parse_top_tens(self, response):
        top_tens = response.css('table.my-segments tbody tr td a::attr(href)').getall()
        self.segments.extend(top_tens)
        next_page = response.xpath('//li[@class="next_page"]/a[@rel="next"]/@href').get()

        # next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield{"next page": next_page}

            # next_href = next_page[0]
            next_page_url = 'https://www.strava.com' + next_page
            yield{"next page": next_page_url}
            yield scrapy.Request(url=next_page_url, callback = self.parse_top_tens)
        for top_ten in self.segments:

            if '/segments/' in top_ten:
                # yield {"top ten": 'https://www.strava.com' + top_ten}
                top_ten = 'https://www.strava.com' + top_ten
                yield{"top ten": top_ten}
                #what if we instead just pass the activity that corresponds to that best spot 
                # yield scrapy.Request(url=top_ten, callback=self.parse_next)

    # def parse_activities(self, response):

    #     links = response.css('a::attr(href)').extract()
    #     for link in links:
    #         if  "/activities" in link:
    #             link = 'https://www.strava.com'+ link
    #             yield { "Activity Links": link}

    #     activity_divs = response.css('div.content.react-feed-component')

    #     # activity_divs = response.css('div.react-feed-container.simple')

    #     for div in activity_divs:
    #         activity_link = div.css('a::attr(href)').get()            
    #         if activity_link:
    #             yield {"activity_link": activity_link}

