# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
import re


class AmzbooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    product_author = scrapy.Field()
    product_price = scrapy.Field()


class Body(scrapy.Item):
    title = scrapy.Field()
    description =scrapy.Field()


class DevBookItem(scrapy.Item):
    links = scrapy.Field()
    abstract_url = scrapy.Field()
    issn_code = scrapy.Field()
    isbn_code = scrapy.Field()
    title = scrapy.Field()
    author_names = scrapy.Field()
    p_name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    load_date = scrapy.Field()
    cited_by = scrapy.Field()
    affil_university = scrapy.Field()
    affil_city = scrapy.Field()
    affil_country = scrapy.Field()


class GscholarItem(scrapy.Item):

    title = scrapy.Field()
    author = scrapy.Field()
    file = scrapy.Field()
    cited_by = scrapy.Field()
    link = scrapy.Field()



