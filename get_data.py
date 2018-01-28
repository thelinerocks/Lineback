import numpy as np
import random
#import matplotlib.pyplot as plt
from database import *
import logging
import time

import redis
logger = logging.getLogger("get_data")

class make_data(object):
    def add_steps(self,data):
        size = int(1/0.05)
        total_array = np.zeros(size)
        for i in range(size):
            total_array[i] = (data[0]) + ((data[1]-data[0])/size)*i
        return total_array

    def get_ticks(self,category, old_total):
        sum_text = get_sum_text(category)
        sum_image = get_sum_image(category)
        total = sum_text + sum_image
        logger.info("Got text,image %.2f, %.2f for %s", sum_text, sum_image, category)
        return self.add_steps([old_total,total])

def add_to_points_list(r, key, val):
    r.lpush(key, val)
    if r.llen(key) > 1000:
        r.rpop(key)

if __name__=="__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        keys = r.keys(pattern="points-*")
        outputs = {}
        for k in keys:
            category = k.decode("utf-8").partition("-")[2]
            md = make_data()
            old_total = r.lindex(k, 0) or 0
            ticks = md.get_ticks(category, float(old_total))
            outputs[k] = ticks

        for i in range(20):
            time.sleep(0.05)
            for k in keys:
                add_to_points_list(r, k, outputs[k][i])

"""
#!/bin/bash

import redis
import random
import time
import logging

logger = logging.getLogger("provider")

if __name__=="__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    val = 0
    hashtag1 = "points-ichackupper"
    hashtag2 = "points-ichacklower"

    while True:
        time.sleep(0.05)
        val = random.random()*5
        r.lpush(hashtag1, val)
        if r.llen(hashtag1) > 1000:
            r.rpop(hashtag1)

        val = random.random()*5
        r.lpush(hashtag2, val)
        if r.llen(hashtag2) > 1000:
            r.rpop(hashtag2)
        logger.debug("Sent datapoints - q length %d", r.llen(hashtag2))
"""
