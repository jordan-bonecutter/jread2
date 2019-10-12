#
#
#
#

from nodetype import nodetype

def get_netw_time(crawl) -> dict:
  ret = {}
  t, f = 0, 0
  for site, data in crawl.items():
    ret[site] = {'total_time': 0, 'ad_time': 0, 'ad_plus_inherited': 0}
    for snap in data['snapshots']:
      for layer in snap['tree_full']:
        for url, info in layer.items():
          t += 1
          if 'timing' not in info:
            f += 1
            continue
          ret[site]['total_time'] += info['timing'] / len(data['snapshots'])
          if info['ad'] != 'no':
            ret[site]['ad_plus_inherited'] += info['timing'] / len(data['snapshots'])
            if info['ad'] == 'yes':
              ret[site]['ad_time'] += info['timing'] / len(data['snapshots'])

  for site in ret.keys():
    try:
      ret[site]['ad_ratio'] = ret[site]['ad_time']/ret[site]['total_time']
    except ZeroDivisionError:
      ret[site]['ad_ratio'] = 0.
    try:
      ret[site]['ad_plus_inherited_ratio'] = ret[site]['ad_plus_inherited']/ret[site]['total_time']
    except ZeroDivisionError:
      ret[site]['ad_plus_inherited_ratio'] = 0.

  return ret, f/t

def get_num_ctypes(crawl) -> dict:
  ret = {}
  for site, data in crawl.items():
    for snap in data['snapshots']:
      for layer in snap['tree_full']:
        for url, info in layer.items():
          ctype = nodetype(info)
          if ctype not in ret:
            ret[ctype] = {'total': 0., 'ad': 0., 'ad_plus_inherited': 0.}
          ret[ctype]['total'] += 1./len(data['snapshots'])
          if info['ad'] != 'no':
            ret[ctype]['ad_plus_inherited'] += 1./len(data['snapshots'])
            if info['ad'] == 'yes':
              ret[ctype]['ad'] += 1./len(data['snapshots'])
  return ret

def main(argv) -> int:
  if len(argv) != 2:
    return 0
  
  with open(argv[1], 'r') as fi:
    crawl = json.load(fi) 
  
  pprint(get_netw_time(crawl))
  pprint(get_num_ctypes(crawl))
  return 0

if __name__ == '__main__':
  import json
  import sys
  from pprint import pprint
  main(sys.argv)
