import scrapy

from racingpost import items


class HorseSpider(scrapy.Spider):

    name = 'horse'
    handle_httpstatus_list = [404]

    def __init__(self, date, *args, **kwargs):
        super(HorseSpider, self).__init__(*args, **kwargs)
        self.date = date
        self.domain = 'www.racingpost.com'
        self.start_urls = [
            'http://{domain}/horses2/cards/home.sd?r_date={date}'.format(
                domain=self.domain, date=date)
        ]

    def parse(self, response):
        cards_path = '//table[@class="cardsGrid"]//td[1]/a/@href'
        for url in response.xpath(cards_path).extract():
            yield scrapy.Request(
                'http://{domain}{url}'.format(domain=self.domain, url=url),
                callback=self.parse_card)

    def parse_card(self, response):

        racename_part_1 = response.xpath(
            '//div[@class="pageHeader cardHeader"]//div[@class="info"]/p'
            '//strong[@class="uppercase"]/text()').extract()
        racename_part_2 = response.xpath(
            '//div[@class="pageHeader cardHeader"]//div[@class="info"]/p'
            '/strong/text()').extract()
        racename_part_3 = response.xpath(
            '//div[@class="pageHeader cardHeader"]//div[@class="info"]/p'
            '/text()[2]').extract()
        format_text = lambda text: text[0].strip().encode('UTF-8') if text else ''
        racename = '{} {} {}'.format(
            format_text(racename_part_1), 
            format_text(racename_part_2),
            format_text(racename_part_3)
        )

        horse_path = '//table[@id="sc_horseCard"]//'\
            'a[@title="Full details about this HORSE"]/@href'
        for url in response.xpath(horse_path).extract():
            request = scrapy.Request(url, callback=self.parse_horse)
            request.meta['racename'] = racename
            request.meta['bestodds'] = ''
            yield request

    def parse_horse(self, response):

        horsename = unicode(response.xpath(
            '//div[@id="otherHorses"]//option[@selected]/text()').extract()[0])

        wgts_path = '//div[@id="horse_form"]//table//tr[@id][@class="fl_F"]/td[4]/text()'
        wgts = [wgt.strip() for wgt in response.xpath(wgts_path).extract()[:5]]

        print 'horsename', horsename

        request = scrapy.http.FormRequest(
            'http://www.pedigreequery.com/cgi-bin/new/check2.cgi',
            formdata={
                 'g': '5',
                 'h': horsename,
                 'inbred': 'Standard',
                 'query_type': 'check',
                 'search_bar': 'horse',
                 'wsid': '1428325537',
                 'x2': 'n'
            },
            callback=self.parse_horse_stat,
        )
        request.meta['racename'] = response.meta['racename']
        request.meta['bestodds'] = response.meta['bestodds']
        request.meta['horsename'] = horsename
        request.meta['wgts'] = wgts
        yield request

    def parse_horse_stat(self, response):

        horsestats_path = 'normalize-space(//table//center/table[1]//center)'
        horsestats = unicode(response.xpath(horsestats_path).extract()[0])

        print items.HorseItem(
            racedate=self.date,
            racename=response.meta.get('racename'),
            bestodds=response.meta.get('bestodds'),
            horsename=response.meta.get('horsename'),
            wgts=response.meta.get('wgts'),
            horsestats=horsestats,
        )
        print 'url', response.url

        yield items.HorseItem(
            racedate=self.date,
            racename=response.meta.get('racename'),
            bestodds=response.meta.get('bestodds'),
            horsename=response.meta.get('horsename'),
            wgts=response.meta.get('wgts'),
            horsestats=horsestats,
        )

# http://www.racingpost.com/horses2/cards/card.sd
# horsename "//table[@id='sc_horseCard']//a[@title]/b/text()"
# date "//div[contains(@class,'raceTitle')]//span[@class='date']/text()" WEDNESDAY, 08 APRIL 2015
# WGT "//div[@id='horse_form']//table//tr[@id][@class='fl_F']/td[4]/text()" 9-4

# http://www.pedigreequery.com/half+a+billion
# "//table//center/table[1]//center/font/text()"   "(IRE) b. G, 2009
#                              {7} DP = 5-1-2-0-0 (8)  DI = 7.00   CD = 1.38 
