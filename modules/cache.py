import redis
import logging
import os
import sys

from modules import parameters

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_cache_connected(rds):
    try:
        rds.client_list()
    except redis.ConnectionError:
        return False
    return True


def connect_to_cache():
    config = parameters.get_redis_config()

    rds = redis.StrictRedis(
        host=config['hostname'],
        password=config['password'],
        port=int(config['port']),
        db=0,
        socket_connect_timeout=5
    )

    connected = is_cache_connected(rds)
    if connected:
        logging.info('Connected to cache.')
        return rds
    else:
        logging.info('Could not connect to redis cache.')
        sys.exit()
