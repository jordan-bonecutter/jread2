#
#
#
#

from nodetype import nodetype

def get_netw_time(crawl) -> dict:
  # return dictionary
  ret = {}

  # loop thru the whole crawl
  for site, data in crawl.items():
    # foreach site, record total time and time for ads
    ret[site] = {'total_time': 0, 'ad_time': 0, 'ad_plus_inherited': 0}
    for snap in data['snapshots']:
      for layer in snap['tree_full']:
        for url, info in layer.items():
          # if the current node has no timing info (< 2%)
          # then skip it
          if 'timing' not in info:
            continue
          ret[site]['total_time'] += info['timing'] / len(data['snapshots'])
          if info['ad'] != 'no':
            ret[site]['ad_plus_inherited'] += info['timing'] / len(data['snapshots'])
            if info['ad'] == 'yes':
              ret[site]['ad_time'] += info['timing'] / len(data['snapshots'])

  # calculate the ratios
  for site in ret.keys():
    try:
      ret[site]['ad_ratio'] = ret[site]['ad_time']/ret[site]['total_time']
    except ZeroDivisionError:
      ret[site]['ad_ratio'] = 0.
    try:
      ret[site]['ad_plus_inherited_ratio'] = ret[site]['ad_plus_inherited']/ret[site]['total_time']
    except ZeroDivisionError:
      ret[site]['ad_plus_inherited_ratio'] = 0.

  return ret

def get_num_ctypes(crawl) -> dict:
  # return dictionary
  ret = {}

  # loop thru the crawls
  for site, data in crawl.items():
    for snap in data['snapshots']:
      for layer in snap['tree_full']:
        for url, info in layer.items():
          # get the content type
          ctype = nodetype(info)
          if ctype not in ret:
            # for each content type, gather total# and #related to ads
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
