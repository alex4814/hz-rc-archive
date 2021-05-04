from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class RcLoader(ItemLoader):
    default_output_processor = TakeFirst()
