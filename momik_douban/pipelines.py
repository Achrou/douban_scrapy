# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MomikDoubanPipeline(object):
    def process_item(self, item, spider):
        return item


class RecordSpiderPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_coll, mongo_user, mongo_psw):
        # 链接数据库
        client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_psw)
        self.db = client[mongo_db]
        self.coll = self.db[mongo_coll]
        # 删除全部电影记录
        self.coll.delete_many({})
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_coll=crawler.settings.get('MONGO_COLL'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_psw=crawler.settings.get('MONGO_PSW'),
        )

    def process_item(self, item, spider):
        postItem = dict(item)
        self.coll.update_one({'title': postItem['title']}, {'$set': postItem}, upsert=True)
        return item
