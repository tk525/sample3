import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://sample301-20210223.herokuapp.com:6379')
# DATABASE_URL = os.environ.get('DATABASE_URL')

conn = redis.from_url(redis_url)
# conn = redis.from_url('https://sample301-20210223.herokuapp.com/twmc_p', db=DATABASE_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
