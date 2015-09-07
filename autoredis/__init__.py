"""
Auto balance your redis command on the slaves/master of your redis infrastructure
"""

from sys import version_info

from redis.sentinel import Sentinel, MasterNotFoundError, SlaveNotFoundError
from redis import StrictRedis
from redis import ConnectionError as RedisConnectionError

__version__ = '0.1.0'

RO_FUNC = [
    'bitcount',
    'bitpos',
    'dump',
    'echo',
    'exists',
    'georadius',
    'georadiusbymember',
    'get',
    'getbit',
    'getrange',
    'hexists',
    'hget',
    'hgetall',
    'hkeys',
    'hlen',
    'hmget',
    'hstrlen',
    'hvals',
    'keys',
    'lindex',
    'llen',
    'lrange',
    'mget',
    'pfcount',
    'pttl',
    'randomkey',
    'scard',
    'sdiff',
    'sdiffstore',
    'sinter',
    'sismember',
    'smembers',
    'srandmember',
    'strlen',
    'sunion',
    'ttl',
    'type',
    'zcard',
    'zcount',
    'zlexcount',
    'zrange',
    'zrangebylex',
    'zrevrangebylex',
    'zrangebyscore',
    'zrank',
    'zrevrange',
    'zrevrangebyscore',
    'zrevrank',
    'zscore'
]

RW_FUNC = [
    'append',
    'bitop',
    'blpop',
    'brpop',
    'brpoplpush',
    'decr',
    'decrby',
    'delete',
    'expire',
    'expireat',
    'flushall',
    'flushdb',
    'geoadd',
    'getset',
    'hdel',
    'hincrby',
    'hincrbyfloat',
    'hmset',
    'hset',
    'hsetnx',
    'incr',
    'incrby',
    'incrbyfloat',
    'linsert',
    'lpop',
    'lpush',
    'lpushx',
    'lrem',
    'lset',
    'ltrim',
    'move',
    'mset',
    'msetnx',
    'persist',
    'pexpire',
    'pexpireat',
    'pfadd',
    'pfmerge',
    'psetex',
    'rename',
    'renamenx',
    'restore',
    'rpop',
    'rpoplpush',
    'rpush',
    'rpushx',
    'sadd',
    'set',
    'setbit',
    'setex',
    'setnx',
    'setrange',
    'sinterstore',
    'smove',
    'sort',
    'spop',
    'srem',
    'sunionstore',
    'zadd',
    'zincrby',
    'zinterstore',
    'zrem',
    'zremrangebylex',
    'zremrangebyrank',
    'zremrangebyscore',
    'zunionstore'
]

class AutoRedis(object):
    """
    AutoRedis main class
    """

    def __getattr__(self, func):
        if func in RO_FUNC:
            self._method = func
            return self._ro_call
        elif func in RW_FUNC:
            self._method = func
            return self._rw_call
        else:
            raise AttributeError(func)

    def __init__(self, master, slaves=None, **kwargs):
        self._method = None
        self._setup_redis(master=master, slaves=slaves, **kwargs)

    def _setup_redis(self, master, slaves=None, **kwargs):
        """
        Setup the redis servers
        """
        self._master = (master, StrictRedis(host=master[0], port=master[1], **kwargs))

        if not slaves:
            self._slaves = None
            return

        self._slaves = []
        for slave in slaves:
            redis_conn = StrictRedis(host=slave[0], port=slave[1], **kwargs)
            self._slaves.append((slave, redis_conn))

    def _ro_call(self, *args, **kwargs):
        """
        Call the method on one of the slave
        """
        while self._slaves:
            slave = self._slaves.pop(0)
            try:
                method = getattr(slave[1], self._method)
            except AttributeError:
                raise
            try:
                data = method(*args, **kwargs)
                self._slaves.append(slave)
                return data
            except (RedisConnectionError, ConnectionRefusedError):
                pass
        return self._rw_call(*args, **kwargs)

    def _rw_call(self, *args, **kwargs):
        """
        Call the method on the master
        """
        try:
            method = getattr(self._master[1], self._method)
        except AttributeError:
            raise
        return method(*args, **kwargs)

    def on_master(self, command, *args, **kwargs):
        """
        Explicitly call the method on the master
        """
        try:
            method = getattr(self._master[1], command)
        except AttributeError:
            raise
        return method(*args, **kwargs)

    def on_slave(self, slave_addr, command, *args, **kwargs):
        """
        Explicitly call the method on the provided slave
        """
        selected_slave = None
        for slave in self._slaves:
            if slave_addr == slave[0]:
                selected_slave = slave
                break
        if not selected_slave:
            raise SlaveNotFoundError

        print(selected_slave[0])
        try:
            method = getattr(selected_slave[1], command)
        except AttributeError:
            raise
        return method(*args, **kwargs)

    @property
    def master(self):
        """
        Return the current master
        """
        return self._master[0]

    @property
    def slaves(self):
        """
        Return the current slave(s)
        """
        if not self._slaves:
            return None
        ret = []
        for slaves in self._slaves:
            ret.append(slaves[0])
        return ret

class AutoRedisSentinel(AutoRedis):
    """
    Auto configure autoredis via redis-sentinel
    """
    def __init__(self, sentinels, service, **kwargs):
        sentinel = Sentinel(sentinels, **kwargs)
        try:
            master = sentinel.discover_master(service)
        except MasterNotFoundError:
            raise
        try:
            slaves = sentinel.discover_slaves(service)
        except SlaveNotFoundError:
            self._slaves = None
        if version_info[0] < 3:
            super(AutoRedisSentinel, self).__init__(master, slaves=slaves, **kwargs)
        else:
            super().__init__(master, slaves=slaves, **kwargs)
