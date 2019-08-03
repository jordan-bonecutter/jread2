# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# filehelper.py # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import json
try:
  import _pickle as pickle
except:
  import pickle
import os

class InvalidPathError(RuntimeError):
    def __init__(self):
        pass

def json_save(js, fname):
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + "/__" + base

    try:
        with open(tname, "w") as fi:
            json.dump(js, fi)
    except TypeError:
        os.remove(tname)
    os.rename(tname, fname)

def pickle_save(obj, fname):
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + "/__" + base

    try:
        with open(tname, "wb") as fi:
            pickle.dump(obj, fi, -1)
    except TypeError:
        os.remove(tname)
    os.rename(tname, fname)
