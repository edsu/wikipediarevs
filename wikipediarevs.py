#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
import pathlib
import argparse
import requests

from urllib.parse import urlparse

def main():
    parser = argparse.ArgumentParser(description="Download Wikipedia article revisions")
    parser.add_argument("input", type=str, help="A Wikipedia article URL or a file that contains Wikipedia URLs.")
    parser.add_argument("--output-dir", default="revisions", type=str, help="The path to a directory where to write results.")
    parser.add_argument("--log", type=str, default="wikipediarevs.log", help="Where to write a log file.")
    parser.add_argument("--quiet", action="store_true", help="Don't print progress to the console.")
    opts = parser.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO)

    # get the input URL
    if os.path.isfile(opts.input):
        urls = open(opts.input).read().splitlines()
    else:
        urls = [opts.input]

    revd = RevisionDownloader(urls, output_dir=opts.output_dir, quiet=opts.quiet)
    revd.run()


class RevisionDownloader:

    def __init__(self, urls, output_dir="revisions", quiet=False):
        self.urls = urls
        self.quiet = quiet
        self.output_dir = pathlib.Path(output_dir)
        if not self.output_dir.is_dir():
            self.output_dir.mkdir(parents=True)

    def run(self):
        for article_url in self.urls:
            self.download(article_url)

    def download(self, article_url):
        logging.info("downloading revisions for %s", article_url)
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

        # if we have files already just get up to the latest one rather than
        # redownloading all of them
        latest_rev_id = self.latest_rev_id(self.output_dir / host / title)
        if latest_rev_id is not None:
            logging.info("only fetching until %s", latest_rev_id)
            params["rvendid"] = latest_rev_id

        while True:
            resp = requests.get(api_url, params=params).json()
            self.write_revisions(resp, host)

            # if there are more results get them
            if 'continue' in resp:
                params['rvcontinue'] = resp['continue']['rvcontinue']
                time.sleep(.5)
            else:
                break

    def write_revisions(self, resp, host):
        """Write a JSON file for each revision using the API response.
        """
        page_id = list(resp["query"]["pages"].keys())[0]
        page = resp["query"]["pages"][page_id]

        if "revisions" not in page:
            logging.warn("No revisions in %s", json.dumps(resp))
            return 

        for rev in page["revisions"]:
            title = page["title"].replace(" ", "_")
            path = self.output_dir / host / title / f"{rev['revid']}.json"
            if not path.parent.is_dir():
                path.parent.mkdir(parents=True)
            json.dump(rev, path.open('w'), indent=2)
            if not self.quiet:
                print(path)

    def latest_rev_id(self, article_dir):
        if not article_dir.is_dir():
            return None
        revs = sorted(map(lambda d: int(d.name.replace(".json", "")), article_dir.iterdir()))
        return revs[-1]

if __name__ == "__main__":
    main()
