# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# adbrowser.py  # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import filehelper
from dbprint import dbprint
import zbrowse
import json
import treehelper
import drawtree
import re
import subprocess
import os
import shutil
from collections import OrderedDict
from EvaluatePerformance import EvaluatePerformance

__chrome_path__ = "/home/behnam/Desktop/webKitProject/chromium/src/out/first_build/chrome"
time_max = 120

class ParseError(RuntimeError):
    def __init__(self):
        pass

class Crawler:
    sites = None
    data  = None
    ofile = None

    def __init__(self, **kwargs):
        if "sites" in kwargs:
            self.sites = kwargs["sites"]
        else:
            self.sites = []

        if "data" in kwargs:
            try:
                with open(kwargs["data"], "r") as fi:
                    self.data = json.load(fi)
            except FileNotFoundError:
                self.data = {}
            except json.JSONDecodeError:
                dbprint("data file " + str(kwargs["data"]) + " not a json file")
                self.data = {}
        else:
            self.data = {}

        if "ofile" in kwargs:
            self.ofile = kwargs["ofile"]
        else:
            self.ofile = "res/crawl.json"

        for site in self.sites:
            if site in self.data:
                continue
            self.data.update({site: {"snapshots": [], "timer": 45}})

    @classmethod
    def fromfile(cls, fname):
        try:
            with open(fname, "r") as fi:
                return cls(**json.load(fi))
        except json.JSONDecodeError:
            dbprint("file " + fname + " is not a json file")
            raise ParseError()

    def __str__(self):
        ret = "Crawler object:\n"
        ret += "sites = " + str(self.sites) + "\n"
        ret += "data  = " + (str(self.data))[:20] + "...\n"
        ret += "ofile = " + self.ofile 
        return ret

    def crawl(self, **kwargs):
        try:
            port = kwargs["port"]
        except KeyError:
            port = 9222

        try:
            draw = kwargs["draw"]
        except KeyError:
            draw = False

        try:
            perfFile = open(kwargs["perfFile"],'w+')
        except KeyError:
            perfFile = None

        try:
            chrome = subprocess.Popen((__chrome_path__, "--headless", "--remote-debugging-port="+str(port), "--disable-gpu", "--no-sandbox", "--disk-cache-size=1", "--disable-gpu-program-cache", "--media-cache-size=1", "--aggressive-cache-discard", "--single-process", "--no-first-run", "--no-default-browser-check", "--user-data-dir=tmp/remote-profile"), stdout=open("./tmp/__chromium_stdout.log", "w"), stderr=open("./tmp/__chromium_stderr.log", "w"))
            counter = 0
            while True:
                for site in self.sites:
                    counter += 1
                    if counter % 10 is 0:
                        self.save(self.ofile)
                    try:
                        tree, performance = zbrowse.get(domain = site, timeout = self.data[site]["timer"], port=port)
                    except zbrowse.Timeout as e:
                        dbprint("Zbrowse timed out in " + str(e.timer) + "s at site " + site) 
                        if self.data[site]["timer"]*2 < time_max:
                            self.data[site]["timer"] *= 2
                        else:
                            self.data[site]["timer"] = time_max
                    except zbrowse.OutOfMemory:
                        dbprint("ZBrowse ran out of memory at site " + site)
                    except zbrowse.IncompleteTree:
                        dbprint("Error parsing json from zbrowse at site " + site)
                    else:
                        dbprint("snapshot at " + site + " was succesful!")
                        trees = treehelper.get_tree(tree, performance)
                        dbprint("raw depth = " + str(treehelper.get_raw_depth(tree)))
                        dbprint("new depth = " + str(len(trees["tree_full"])))
                        self.data[site]["snapshots"].append(trees)
                        l = len(self.data[site]["snapshots"])
                        if perfFile:
                          try:
                            trace_path = os.path.join("./trace", site+"_"+str(l))
                            shutil.move('trace.json',trace_path)
                          except:
                            pass
                        if draw:
                            dbprint("drawing full")
                            drawtree.draw_tree(trees["tree_full"], "res/img/"+site+str(l)+"full.pdf")
                            dbprint("drawing trim")
                            drawtree.draw_tree(trees["tree_trim"], "res/img/"+site+str(l)+"trim.pdf")
        except KeyboardInterrupt:
            self.save(self.ofile)
            chrome.kill()
        raise KeyboardInterrupt()

    def save(self, fname):
        filehelper.json_save(self.data, fname)
