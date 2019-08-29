#
#
#
#

import json
from dbprint import dbprint

__magic_string__ = "!@#$!@#$"

def myload(s):
  tmp = ''
  i = 0
  for c in s:
    if c == ':':
      break
    tmp += c
    i += 1

  return {tmp: s[i+1:]}

def parse(output):
    return (json.loads(output), [])

def _hhhparse(output): 
  breakpoint()
  lines = output.split('\n')
  dbprint(str(len(lines)-2) + " performance items logged")
  perf = []
  tree = None
  for i in range(len(lines)-2):
    try:
      perf.append(json.loads(lines[i][len(__magic_string__):])) 
    except json.JSONDecodeError:
      perf.append(myload(lines[i][len(__magic_string__):]))

  tmp  = perf
  perf = {}
  for p in tmp:
    try:
      perf[p['name']] = p
    except KeyError:
      perf.update(p)

  try:
    tree = json.loads(lines[len(lines)-2])
  except json.JSONDecodeError:
    pass
  if tree != None and "_root" not in tree:
    tree = None
  return (tree, perf)
