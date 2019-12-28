import os


def get_redis_config():
    config = {}

    config['hostname'] = os.getenv('REDIS_HOST', '')
    config['port'] = os.getenv('REDIS_PORT', '0')
    config['password'] = os.getenv('REDIS_PASS', '')

    return config
