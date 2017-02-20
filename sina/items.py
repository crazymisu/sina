# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()
    sub_title = scrapy.Field()
    sub_url = scrapy.Field()
    sub_Filename = scrapy.Field()
    son_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

