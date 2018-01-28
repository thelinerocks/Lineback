# get all public posts from instagram with specified tag
# uses the proxy API from https://github.com/whizzzkid/instagram-proxy-api

import requests
import json
import logging
import time
import urllib.parse as urlparse
import datetime
import sys
import base64
import time

import database


logger = logging.getLogger("lineback.instagram")

def get_instagram_posts(tag, since, host="http://localhost:3000", limit=20):
    endpoint = "{}/explore/tags/{}/media".format(host, tag)
    params = {"count": 100}
    output = []

    try:
        posts = requests.get(endpoint, params=params)
    except requests.RequestException:
        logger.exception("Instagram API is down!")
        return []

    if posts.status_code != 200:
        logger.error("API returned %d code", posts.status_code)
        return []

    posts = posts.json()
    params = urlparse.parse_qs(urlparse.urlparse(posts["next"]).query)

    if not posts["posts"]:
        return output

    for p in posts["posts"]:
        if len(output) > limit:
            break

        ts = datetime.datetime.utcfromtimestamp(p["taken_at_timestamp"])
        if ts <= since:
            break

        d = {}
        d["date"] = ts
        if ("edge_media_to_caption" in p) and (p["edge_media_to_caption"]["edges"]):
            d["message"] = p["edge_media_to_caption"]["edges"][0]["node"]["text"]
        else:
            d["message"] = ""
        d["image_url"] = p["display_url"]

        d["profile_pic_url"] = ""
        if "thumbnail_resources" in p:
            d["profile_pic_url"] = p["thumbnail_resources"][0]["src"]

        d["social_network"] = "instagram"
        d["user_name"] = "Instagram User"
        output.append(d)
    return output

if __name__=="__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    t = database.get_most_recent("instagram")
    if t is None:
        t = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    logger.info("Polling data since: %s", t.isoformat())

    last = t
    while True:
        l = get_instagram_posts(sys.argv[1], last, host="http://108.61.175.107:3000", limit=20)

        for post in l:
            database.save_post(post)
            if post["date"] > last:
                last = post["date"]

        logger.info("Got %d posts from instagram up to %s", len(l), last.isoformat())
        time.sleep(5)
