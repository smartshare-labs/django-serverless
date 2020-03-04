import json
import os
import time
import uuid
import logging

from modules import cache
from modules import parameters


def run():
    rds = cache.connect_to_cache()
    rds.flushall()

if __name__ == '__main__':
    run()
