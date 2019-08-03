# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# zbrowse.py  # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import subprocess
import os
import signal
import time
from snapfile import SnapFile
from kbinterruptable import kbint
import re
import json
from dbprint import *
import jparse
import time

zbpath = "./util/zbrowse/"
_zout_name = "tmp/__zb_sout.snap"
_zerr_name = "tmp/__zb_serr.snap"

_proc   = []
_files  = []

class Timeout(RuntimeError):
    def __init__(self, timer):
        self.timer = timer

class OutOfMemory(RuntimeError):
    def __init__(self):
        pass

class IncompleteTree(RuntimeError):
    def __init__(self):
        pass

def __cleanup():
    global _proc, _files
    for process in _proc:
      process.kill()
      process.wait()
    for fi in _files:
        fi.close()
    _files = []
    _proc  = []

def __get(*args, **kwargs):
    global zbpath, _zout_name, _zerr_name, _tout_name, _terr_name

    try:
        port = kwargs["port"]
    except KeyError:
        port = 9222
    dbprint("setting up zbrowse at " + str(port))

    # set up local variables
    start = time.time()
    domain = "https://www." + kwargs["domain"]
    zopts = ("node", zbpath+"index.js", domain, str(port))

    # append so cleanup is easier
    zout   = SnapFile.open(_zout_name)
    _files.append(zout)
    zerr   = SnapFile.open(_zerr_name)
    _files.append(zerr)
    z_proc = subprocess.Popen(args = zopts, stdout = zout.fd, stderr = zerr.fd)
    _proc.append(z_proc)

    try:
        z_proc.wait(kwargs["timeout"])
        end = time.time()
        __cleanup()
        chrome_id = int(zerr.contents.split()[0])
        try:
          os.kill(chrome_id, signal.SIGTERM)
        except ProcessLookupError:
          pass 
        if re.search(r"heap out of memory", zerr.contents) is not None:
            raise OutOfMemory()
        try:
            tree = json.loads(zout.contents)
        except json.JSONDecodeError:
            raise IncompleteTree()
    except subprocess.TimeoutExpired:
        end = time.time()
        __cleanup()
        raise Timeout(end-start)

    with open("chrometrace.log", "r") as fi:
        trace = fi.read()
    os.remove("chrometrace.log")
    lines = list(re.findall(r"(?:^|\n)(.+?),(?:$|\n)", trace))
    return (json.loads(zout.contents), [line for line in lines if re.search("(?:url|URL|Url)", line) is not None])

get = kbint(__get, __cleanup)
