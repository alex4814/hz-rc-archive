# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo.errors import DuplicateKeyError
from pymongo.errors import AutoReconnect


class PersistencePipeline:
    database = "hz"
    collection = "gccrc"

    def __init__(self, mongo_uri):
        usr = os.getenv("MONGO_GCCRC_USER", "user")
        pwd = os.getenv("MONGO_GCCRC_PASSWORD", "password")
        self.mongo_uri = mongo_uri.format(usr, pwd)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            self.mongo_uri,
            retryWrites=True,
            w='majority',
            connectTimeoutMS=2000,
        )
        self.db = self.client[self.database]
        self.gccrc = self.db[self.collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        retry = True
        while retry:
            try:
                self.gccrc.insert_one(item_dict)
            except DuplicateKeyError:
                spider.stop_follow = True
                retry = False
                spider.logger.info(f"Duplicate Found: ID {item_dict['_id']}")
            except AutoReconnect:
                spider.logger.warning(f"Connection Failure. Try inserting item again {item_dict}")
            else:
                spider.logger.info(f"Insert hzgccrc {item_dict['name']}")
                retry = False
        return item
