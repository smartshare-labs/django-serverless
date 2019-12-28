import redis
import logging
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
    redis_config = parameters.from_config(
        ["REDIS_HOST", "REDIS_PASSWORD", "REDIS_PORT"]
    )

    rds = redis.StrictRedis(
        host=redis_config["REDIS_HOST"],
        password=redis_config["REDIS_PASSWORD"],
        port=int(redis_config["REDIS_PORT"]),
        db=0,
        socket_connect_timeout=5,
    )

    connected = is_cache_connected(rds)
    if connected:
        logging.info("Connected to cache.")
        return rds
    else:
        logging.info("Could not connect to redis cache.")
        sys.exit()
