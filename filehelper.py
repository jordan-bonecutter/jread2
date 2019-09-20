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
from typing import Any, Callable, Union, NoReturn, IO
import random
import string


def file_save(obj: Any, fname: str, serializer: Union[Callable[[Any, IO], NoReturn]], needsBin: bool) -> NoReturn:
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + '/' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(64))

    if needsBin:
        ostring = 'wb'
    else:
        ostring = 'w'

    if serializer is not None:
        try:
            with open(tname, ostring) as fi:
                serializer(obj, fi)
        except TypeError:
            os.remove(tname)
    else:
        with open(tname, ostring) as fi:
            fi.write(obj)

    os.rename(tname, fname)

def to_json(o, level=0):
    INDENT = 3
    SPACE = " "
    NEWLINE = "\n"
    ret = ""
    if isinstance(o, dict):
        ret += "{" + NEWLINE
        comma = ""
        for k,v in o.items():
            ret += comma
            comma = ",\n"
            ret += SPACE*INDENT*(level+1)
            ret += '"' + str(k) + '":' + SPACE
            ret += to_json(v, level + 1)

        ret += NEWLINE + SPACE*INDENT*level + "}"
        ret += "}"
    elif isinstance(o, str):
        ret += '"' + o + '"'
    elif isinstance(o, list):
        ret += "[" + ",".join([to_json(e, level+1) for e in o]) + "]"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    else:
        ret += 'null'
    return ret


def json_save(js, fname):
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + '/' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

    with open(tname, 'w') as fi:
        json.dump(js, fi, indent = None, separators = (',\n', ': '))
    os.rename(tname, fname)
  
