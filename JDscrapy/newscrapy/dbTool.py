"""这是一个集成数据库连接，插入，删除的工具类。"""
import logging

from pymongo import MongoClient


class MongoDb(object):
    """mongodb的连接类，供外部调用"""

    def __init__(self):
        try:
            mogo_client = MongoClient()
        except Exception as e:
            msg = e.args[0] + 'mongodb数据库连接失败'
            logging.error(msg)
            self.db = None
        else:
            self.db = mogo_client.document

    def insert(self, doc, dic: dict):
        if self.db == None:
            return "fail", "失败，数据库没有连接成功"
        course = self.db[doc]
        course.insert(dic)
        return 'None', "成功"

    def getall(self,doc):
        if self.db == None:
            return "fail", "失败，数据库没有连接成功"
        course = self.db[doc]
        data = course.find()
        return data, "成功"

    def update_one(self, doc, search, dic):
        if self.db == None:
            return "fail", "失败，数据库没有连接成功"
        course = self.db[doc]
        data = course.update(search,dic)
        return data, "成功"