# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field


class SofaridersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_url = Field()
    lastLogin = Field()
    couchStatus = Field()
    location = Field()
    verificationStatus = Field()
    responseRate = Field()
    languages = Field()
    age = Field()
    sex = Field()
    memberSince = Field()
    hometown = Field()
    profileCompletion = Field()
    education = Field()
    maxGuests = Field()
    preferredGender = Field()
    lastMinuteOkay = Field()
    refs_fromSurfers_pos = Field()
    refs_fromSurfers_neg = Field()
    refs_fromHosts_pos = Field()
    refs_fromHosts_neg = Field()
    friends = Field()
