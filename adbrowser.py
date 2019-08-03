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
        except:
            draw = False

        try:
            counter = 0
            while True:
                counter += 1
                if counter % 10 is 0:
                    self.save(self.ofile)
                for site in self.sites:
                    try:
                        data = zbrowse.get(domain = site, timeout = self.data[site]["timer"], port=port)
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
                        trees = treehelper.get_tree(data)
                        dbprint("raw depth = " + str(treehelper.get_raw_depth(data[0])))
                        dbprint("new depth = " + str(len(trees["tree_full"])))
                        self.data[site]["snapshots"].append(trees)
                        l = len(self.data[site]["snapshots"])
                        if draw:
                            dbprint("drawing full")
                            drawtree.draw_tree(trees["tree_full"], "res/img/"+site+str(l)+"full.png")
                            dbprint("drawing trim")
                            drawtree.draw_tree(trees["tree_trim"], "res/img/"+site+str(l)+"trim.png")
        except KeyboardInterrupt:
            self.save(self.ofile)
        raise KeyboardInterrupt()

    def save(self, fname):
        filehelper.json_save(self.data, fname)
