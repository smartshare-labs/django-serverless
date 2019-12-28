import os


def from_config(keys):
    config = {}
    for k in keys:
        config[k] = os.getenv(k, None)
    return config
