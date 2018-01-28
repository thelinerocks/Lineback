# push mentions to redis every so often - see stuff happen

from database import TaggedPost, get_mention
import redis
import logging
import collections
import time

import json

logger = logging.getLogger("get_data")

def push_to_frontend(r, category, m):
    key = "mentions-"+category
    mention = {"linetag": category,
               "category": category,
               "user_name": m.user_name,
               "profile_pic_url": m.profile_pic_url,
               "social_network": m.social_network,
               "message": m.message}

    logger.info("Pushing message from %s/%s", mention["user_name"], mention["social_network"])

    if r.llen(key) < 2.5:
        r.lpush(key, json.dumps(mention))

if __name__=="__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    keys = r.keys("points-*")
    last_pushed = collections.defaultdict(int)

    while True:
        for k in keys:
            category = k.decode("utf-8").partition("-")[2]
            last_idx = last_pushed[k]
            mention = get_mention(category, last_idx)
            if mention is None:
                continue
            last_pushed[k] = mention.id
            push_to_frontend(r, category, mention)
        time.sleep(5)
