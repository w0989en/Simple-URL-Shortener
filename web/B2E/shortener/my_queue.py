from shortener import models
from django.db.models import Max

# import redis
import queue


class PythonQueue(object):
    def __init__(self):
        self.queue_len = 1000
        id_max = models.ShortURL.objects.all().aggregate(Max('id'))['id__max'] + 1
        print('id_max=', id_max)
        self.q = queue.Queue()
        for i in range(self.queue_len):
            self.q.put(i + id_max)

    def put(self, item):
        self.q.put(item)

    def get(self, timeout=10):
        item = self.q.get(timeout=timeout)
        return item


# class RedisQueue(object):
#     def __init__(self, name, namespace='queue', **redis_kwargs):
#         # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
#         self.__db = redis.Redis(**redis_kwargs)
#         self.key = '%s:%s' % (namespace, name)
#
#     def qsize(self):
#         return self.__db.llen(self.key)  # 返回队列里面list内元素的数量
#
#     def put(self, item):
#         self.__db.rpush(self.key, item)  # 添加新元素到队列最右方
#
#     def get_wait(self, timeout=None):
#         # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
#         item = self.__db.blpop(self.key, timeout=timeout)
#         return item
#
#     def get_nowait(self):
#         # 直接返回队列第一个元素，如果队列为空返回的是None
#         item = self.__db.lpop(self.key)
#         return item

