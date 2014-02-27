# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PostItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    url = Field()
    project_name = Field()
    project_address = Field()
    project_investment= Field()
    builder_name = Field()
    builder_address = Field()
    eia_name = Field()
    eia_address = Field()
    page_content = Field()
    pollutions = Field()
    start_date = Field()
    post_start_date = Field()
    post_end_date = Field()

    crawled = Field()
    spider = Field()
