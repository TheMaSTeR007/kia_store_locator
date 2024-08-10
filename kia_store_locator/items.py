# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KiaStoreLocatorItem(scrapy.Item):
    # define the fields for your item here like:
    state_name = scrapy.Field()
    state_key = scrapy.Field()
    city_name = scrapy.Field()
    city_key = scrapy.Field()
    city_url = scrapy.Field()


class KiaDealerDataItem(scrapy.Item):
    state_name = scrapy.Field()
    city_name = scrapy.Field()
    website = scrapy.Field()
    dealer_name = scrapy.Field()
    address1 = scrapy.Field()
    address2 = scrapy.Field()
    address3 = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    city_code = scrapy.Field()
    state_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    sort_id = scrapy.Field()
    dealer_type = scrapy.Field()
    dealer_id = scrapy.Field()
    email = scrapy.Field()
