# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataAnalystItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    job_description = scrapy.Field()
    available_since = scrapy.Field()
