# get all public posts from instagram with specified tag
# uses the proxy API from https://github.com/whizzzkid/instagram-proxy-api

import requests
import json
import logging
import time
import urllib.parse as urlparse

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

        ts = p["taken_at_timestamp"]
        if ts < since:
            break

        d = {}
        if "edge_media_to_caption" in p:
            d["text"] = p["edge_media_to_caption"]["edges"][0]["node"]["text"]
        else:
            d["text"] = ""
        d["url"] = p["display_url"]

        d["thumb_src"] = ""
        if "thumbnail_resources" in p:
            d["thumb_src"] = p["thumbnail_resources"][0]["src"]
        output.append(d)

    print(output)
    return output

if __name__=="__main__":
    get_instagram_posts("theline", time.time()-(60*60*48), host="http://108.61.175.107:3000", limit=20)
