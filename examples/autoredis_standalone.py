import sys

from autoredis import AutoRedis
from redis import ConnectionError as RedisConnectionError
from redis.sentinel import MasterNotFoundError

if __name__ == '__main__':
    try:
        AUTO_REDIS = AutoRedis(('127.0.0.1', 6379), slaves=[('127.0.0.1', 6380)], decode_responses=True)
    except MasterNotFoundError:
        print('No master found')
        sys.exit(1)

    AUTO_REDIS.sadd('myset', 'mydata')
    for i in range(1, 10):
        try:
            print(AUTO_REDIS.smembers('myset'))
            print(AUTO_REDIS.on_master('ping'))
            if AUTO_REDIS.slaves:
                print(AUTO_REDIS.on_slave(('127.0.0.1', 6380), 'ping'))
        except RedisConnectionError:
            print('No slave or master up')
            sys.exit(1)
        print('Slaves: ' + str(AUTO_REDIS.slaves))
