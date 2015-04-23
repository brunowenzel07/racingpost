# -*- coding: utf-8 -*-

import scrapy


class RacingpostHorseItem(scrapy.Item):
    racedate = scrapy.Field()
    racename = scrapy.Field()
    bestodds = scrapy.Field()
    horsename = scrapy.Field()
    wgts = scrapy.Field()
    horsestats = scrapy.Field()


class HkjcHorseItem(scrapy.Item):
    racenumber = scrapy.Field()
    raceindex = scrapy.Field()
    racename = scrapy.Field()
    horsenumber = scrapy.Field()
    horsename = scrapy.Field()
    horsecode = scrapy.Field()
    timelist = scrapy.Field()
    sirename = scrapy.Field()
    racedate = scrapy.Field()
    place = scrapy.Field()
    final_sec_time = scrapy.Field()

class ScmpHorseItem(scrapy.Item):
    racename = scrapy.Field()
    horsenames = scrapy.Field()
    jb_comment = scrapy.Field()
