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
from typing import Any, Callable, Union, IO
import random
import string


def file_save(obj: Any, fname: str, serializer, needsBin: bool):
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + '/' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

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

def to_json(o, level=1):
  ret = ''
  INDENT = '  ' 
  if isinstance(o, dict):
    ret += '{'
    for k, v in o.items():
      ret += '\n' + INDENT*level + to_json(k, level+1) + ': ' + to_json(v, level+1) + ','
    ret = ret[:1 if len(ret) == 1 else len(ret)-1]
    ret += '\n' + INDENT*(level-1) + '}'
  elif isinstance(o, list):
    ret += '['
    for v in o:
      ret += '\n' + INDENT*level + to_json(v, level+1) + ','
    ret = ret[:1 if len(ret) == 1 else len(ret)-1]
    ret += '\n' + INDENT*(level-1) + ']'
  elif isinstance(o, str):
    ret = '"' + o + '"'
  elif isinstance(o, int):
    ret += str(o)
  elif isinstance(o, float):
    ret += str(o)
  elif isinstance(o, bool):
    if o:
      ret += 'true'
    else:
      ret += 'false'
  else:
    ret += 'null'
  return ret


def json_save(js, fname):
    base = os.path.basename(fname)
    path = "./" + os.path.dirname (fname)
    tname = path + '/' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

    todump = to_json(js)

    with open(tname, 'w') as fi:
        fi.write(todump)
    os.rename(tname, fname)
  
