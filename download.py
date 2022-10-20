#!/usr/bin/env python3

import os
import sys
import json
import time
import pathlib
import requests

from urllib.parse import urlparse

output_dir = pathlib.Path("revisions")

def main():
    for article_url in open(sys.argv[1]).read().splitlines():
        download(article_url)

def download(article_url):
    url = urlparse(article_url)
    host = url.netloc
    api_url = f"https://{host}/w/api.php"

    # the article title
    title =  os.path.basename(url.path)

    # The properties to request for each revision:
    # https://en.wikipedia.org/w/api.php?action=help&modules=query%2Brevisions
    props = [
        "ids",
        "flags",
        "timestamp",
        "user",
        "userid",
        "size",
        "slotsize",
        "sha1",
        "slotsha1",
        "contentmodel",
        "comment",
        "parsecomment",
        "content",
        "tags",
        "roles",
        "parsetree",
        "flagged",
        "orescores",
    ]

    # Query parameters for the API call
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvlimit": 500,
        "rvprop": "|".join(props)
    }

    while True:
        resp = requests.get(api_url, params=params).json()
        write_revisions(resp)

        # if there are more results get them
        if 'continue' in resp:
            params['rvcontinue'] = resp['continue']['rvcontinue']
            time.sleep(.5)
        else:
            break

def write_revisions(resp):
    """Write a JSON file for each revision using the API response.
    """
    page_id = list(resp["query"]["pages"].keys())[0]
    page = resp["query"]["pages"][page_id]
    for rev in page["revisions"]:
        title = page["title"].replace(" ", "_")
        path = output_dir / title / f"{rev['revid']}.json"
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True)
        json.dump(rev, path.open('w'), indent=2)
        print(path)

if __name__ == "__main__":
    main()
