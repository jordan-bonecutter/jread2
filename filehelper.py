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

class InvalidPathError(RuntimeError):
    def __init__(self):
        pass


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
