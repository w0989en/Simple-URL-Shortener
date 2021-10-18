from shortener import models
from django.db.models import Max

import redis
import queue


class PythonQueue(object):
    '''
        limit processes = 1
    '''
    def __init__(self):
        self.queue_len = 100
        try:
            id_max = models.ShortURL.objects.all().aggregate(Max('id'))['id__max'] + 1
        except:
            id_max = 1
        print('id_max=', id_max)
        self.q = queue.Queue()
        for i in range(self.queue_len):
            self.q.put(i + id_max)

    def put(self, item):
        self.q.put(item)

    def get(self, timeout=10):
        item = self.q.get(timeout=timeout)
        return item
    
    def qsize(self):
        return self.q.qsize()


class RedisQueue(object):
    def __init__(self, name, namespace='queue'):
        redis_kwargs = {'host': 'redis', 'port': 6379, 'db': 0}
        self.__db = redis.Redis(**redis_kwargs)
        self.__db.flushdb()
        self.key = '%s:%s' % (namespace, name)

        self.queue_len = 100
        try:
            id_max = models.ShortURL.objects.all().aggregate(Max('id'))['id__max'] + 1
        except:
            id_max = 1
        print('id_max=', id_max)
        for i in range(self.queue_len):
            self.__db.rpush(self.key, i+id_max)

    def qsize(self):
        return self.__db.llen(self.key)

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get(self, timeout=5):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    def get_nowait(self):
        # return None if empty
        item = self.__db.lpop(self.key)
        return item
