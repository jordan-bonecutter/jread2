#
#
#
#

from treehelper import get_url as get_domain

def calculateByDomain(crawl):
  # return dicts
  ret = {}
  total = 0

  # loop through entire crawl
  for site, data in crawl.items():
    for snap in data['snapshots']:
      for level in snap['tree_full']:
        for url, info in level.items():
          # only do anything if current node has timing data
          if 'timing' in info:
            domain = get_domain(url)
            total += info['timing']/len(data['snapshots'])
            if domain in ret:
              ret[domain]['total'] += info['timing']/len(data['snapshots'])
            else:
              ret[domain] = {'total': info['timing']/len(data['snapshots'])}

  # calculate the ratio of time spent in that site
  for domain in ret.keys():
    ret[domain]['ratio'] = ret[domain]['total']/total

  return ret
