# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class EpisodeItem(Item):
    cont_id = Field()       # necessary
    site_id = Field()       # necessary
    title = Field()
    url = Field()           # necessary
    thumb_url = Field()
    duration = Field()
    cp_name = Field()
    tag = Field()
    played = Field()
    utime = Field()
    channel_name = Field()    # necessary
    priority = Field()


