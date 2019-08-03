import json

with open("res/crawl.json", "r") as fi:
  crawls = json.load(fi)

ad_types = {}
for site, data in crawls.items():
  for snap in data["snapshots"]:
    for level in snap["tree_full"]:
      for url, data in level.items():
        if data["ad"] != "yes":
          continue
        try:
          ad_types[data["type"]].append(url)
        except KeyError:
          ad_types.update({data["type"]: [url]})

tmp = []
for t, urls in ad_types.items():
  tmp.append((t, urls))
ad_types_sorted = sorted(list(tmp), key=lambda t: len(t[1]))
del tmp

for t in ad_types_sorted:
  print(str(t[0]) + " - " + str(len(t[1])))
