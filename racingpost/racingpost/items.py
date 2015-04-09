# -*- coding: utf-8 -*-

import scrapy


class HorseItem(scrapy.Item):
    racedate = scrapy.Field()
    racename = scrapy.Field()
    bestodds = scrapy.Field()
    horsename = scrapy.Field()
    wgts = scrapy.Field()
    horsestats = scrapy.Field()
