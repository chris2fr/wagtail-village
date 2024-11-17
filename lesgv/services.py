# import asyncio
import json
import os
import time
import urllib.parse

import requests


# import xmlrpc.client


def get_blog_posts(params={}):
    # url = 'https://blog.lesgrandsvoisins.com/ghost/api/content/posts/?key=1c04bede3eb01bfb3fb106b902'
    url = "https://blog.lesgrandsvoisins.com/ghost/api/content/posts/?key=2c45719752e391ac90cbab9b91"
    # print(url)
    filenametime = "./cache/cache-blog.lesgrandsvoisins.com-" + time.strftime("%Y-%m-%d-%H")
    filenamedate = "./cache/cache-blog.lesgrandsvoisins.com-" + time.strftime("%Y-%m-%d")
    for i in ["limit", "order", "filter", "page", "formats", "include"]:
        if params.get("ghost_{}".format(i), False):
            filenametime += "-{}_{}".format(i, urllib.parse.quote("{}".format(params.get("ghost_{}".format(i)))))
            filenamedate += "-{}_{}".format(i, urllib.parse.quote("{}".format(params.get("ghost_{}".format(i)))))
            url += "&{}={}".format(i, urllib.parse.quote("{}".format(params.get("ghost_{}".format(i)))))
    filenametime += ".json"
    filenamedate += ".json"
    if os.path.isfile(filenametime):
        ret = json.load(open(filenametime))
        return ret
    if os.path.isfile(filenamedate):
        ret = json.load(open(filenamedate))
        os.remove(filenamedate)
        return ret
    response = requests.get(url)
    # print(url)
    ret = response.json()["posts"]
    for i in range(len(ret)):
        if ret[i]["feature_image"]:
            ret[i]["feature_image_1000"] = ret[i]["feature_image"].replace(
                "/content/images/", "/content/images/size/w1000/"
            )
            ret[i]["feature_image_300"] = ret[i]["feature_image"].replace(
                "/content/images/", "/content/images/size/w300/"
            )
            ret[i]["feature_image_600"] = ret[i]["feature_image"].replace(
                "/content/images/", "/content/images/size/w600/"
            )
    print(filenametime)
    with open(filenametime, "w") as outfile:
        json.dump(ret, outfile)
    with open(filenamedate, "w") as outfile:
        json.dump(ret, outfile)
    return ret


def ProcessGhostParams(value={}):
    post_filter = value.get("post_filter") or ""
    if post_filter != "" and value.get("ghost_tag"):
        post_filter += ","
    if value.get("ghost_tag"):
        post_filter += "primary_tag:{}".format(value.get("ghost_tag"))
    params = {
        "ghost_limit": value.get("ghost_limit") or 15,
        "ghost_include": value.get("ghost_include") or "tags,authors",
        "ghost_order": value.get("ghost_order") or "",
        "ghost_filter": post_filter,
        "ghost_page": "{}".format(value.get("ghost_page") or 1),
    }
    return params


# def get_events(params={}):
#     info = xmlrpc.client.ServerProxy('https://ooo.lesgrandsvoisins.com.com/start').start()
#     url, db, username, password = info['host'], info['database'], info['user'], info['password']
