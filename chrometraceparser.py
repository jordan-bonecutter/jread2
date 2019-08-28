#
#
#
#

import json
import re

def get_unique_urls(fname):
  with open(fname, "r") as fi:
    contents = fi.read()

  matches = re.findall(r"\"(http.*?)\"", contents)
  ret = set()

  for match in matches:
    ret |= {match}

  return ret
  

def parse(fname):
  with open(fname, "r") as fi:
    contents = json.load(fi)

  if isinstance(contents, dict):
    contents = contents["traceEvents"]
  byurl = {}
  r_ids = {}
  byrid = {}
  for event in contents:
    if event["name"] == "ResourceSendRequest":
      r_ids.update({event["args"]["data"]["requestId"]: event["args"]["data"]["url"]})
      if event["args"]["data"]["requestId"] in byrid:
        if byurl[event["args"]["data"]["url"]] == None:
          byurl[event["args"]["data"]["url"]] = []
        for e in byrid[event["args"]["data"]["requestId"]]:
          byurl[event["args"]["data"]["url"]].append(e)
        del byrid[event["args"]["data"]["requestId"]]

      try:
        byurl[event["args"]["data"]["url"]].append(event)
      except KeyError:
        byurl[event["args"]["data"]["url"]] = [event]
    elif event["name"] == "ResourceFinish":
      try:
        byurl[r_ids[event["args"]["data"]["requestId"]]].append(event)
      except KeyError:
        try:
          byrid[event["args"]["data"]["requestId"]].append(event)
        except KeyError:
          byrid[event["args"]["data"]["requestId"]] = [event]

  ret = {}
  for url, events in byurl.items():
    st = 9999999999999999
    en = 0
    for event in events:
      st = min(st, event["ts"])
      en = max(en, event["ts"])

    ret[url] = en - st

  return ret
  
