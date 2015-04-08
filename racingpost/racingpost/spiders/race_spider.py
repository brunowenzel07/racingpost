import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule


class RaceSpider(scrapy.Spider):

    name = 'race'
    allowed_domains = ['racingpost.com']
    start_urls = [
        'http://www.racingpost.com/horses2/cards/home.sd?r_date=2015-04-08'
    ]

    def parse(self, response):
        filename = '/home/himik/racingpost/data/race'
        with open(filename, 'wb') as f:
            f.write(response.body)

# http://www.racingpost.com/horses2/cards/card.sd
# horsename "//table[@id='sc_horseCard']//a[@title]/b/text()"
# date "//div[contains(@class,'raceTitle')]//span[@class='date']/text()" WEDNESDAY, 08 APRIL 2015
# WGT "//div[@id='horse_form']//table//tr[@id][@class='fl_F']/td[4]/text()" 9-4

# http://www.pedigreequery.com/half+a+billion
# "//table//center/table[1]//center/font/text()"   "(IRE) b. G, 2009
#                              {7} DP = 5-1-2-0-0 (8)  DI = 7.00   CD = 1.38 