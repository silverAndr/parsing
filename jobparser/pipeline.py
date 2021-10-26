from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_280

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        if collection.insert_one(item):
            print('saved')
        return item
