#
#
#
#

import json
from dbprint import dbprint

__magic_string__ = "!@#$!@#$"

def parse(output): 
  lines = output.split('\n')
  dbprint(str(len(lines)-2) + " performance items logged")
  perf = []
  tree = None
  for i in range(len(lines)-2):
    try:
      perf.append(json.loads(lines[i][len(__magic_string__):])) 
    except json.JSONDecodeError:
      pass

  tmp  = perf
  perf = {}
  for p in tmp:
    perf[p['name']] = p

  try:
    tree = json.loads(lines[len(lines)-2])
  except json.JSONDecodeError:
    pass
  if "_root" not in tree:
    tree = None
  return (tree, perf)
