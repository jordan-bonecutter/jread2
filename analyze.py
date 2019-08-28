import json

def get_related_ad_activities(c):
  ret = {}
  for domain, ddata in c.items():
    for snap in ddata["snapshots"]:
      for level in snap["tree_full"]:
        for url, info in level.items():
          if info["ad"] == "yes":
            try:
              ret[url].append(info["relatedEvents"])
            except KeyError:
              ret[url] = [info["relatedEvents"]]

  return ret
