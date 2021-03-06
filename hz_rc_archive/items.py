# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HzRcArchiveItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    company = scrapy.Field()
    level = scrapy.Field()
    qualification = scrapy.Field()
