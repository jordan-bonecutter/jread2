# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main.py # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from adbrowser import Crawler
import sys
import threading
from dbprint import dbprint

def main(argv):
    try:
        if "-q" in argv:
            dbprint.should_print = False
        dbprint("Starting from main")
        crawler = Crawler.fromfile("setup_files/options.json")
        crawler.crawl(port=9222, draw=True)
    except KeyboardInterrupt:
        print()
        dbprint("main interrupted, shutting down")
        return 0

if __name__ == "__main__":
    main(sys.argv)
