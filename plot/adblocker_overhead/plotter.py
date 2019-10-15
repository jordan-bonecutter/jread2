import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

with open('ext_info8.json', 'r') as fi:
  ext_info = json.load(fi)
with open('nxt_info8.json', 'r') as fi:
  nxt_info = json.load(fi)

ext_times = {}
ext_avg = 0.
for key, items in ext_info.items():
  val = 0.
  n   = 0
  for item in items:
    if 'load' in item:
      val += float(item[6:-2]) 
      n   += 1
  try:
    ext_times[key] = val / n
    ext_avg += val / n
  except ZeroDivisionError:
    pass
ext_avg /= len(ext_times)

nxt_times = {}
nxt_avg = 0.
for key, items in nxt_info.items():
  val = 0.
  n   = 0
  for item in items:
    if 'load' in item:
      val += float(item[6:-2])     
      n   += 1 
  try:
    nxt_times[key] = val / n
    nxt_avg += val / n
  except ZeroDivisionError:
    pass
nxt_avg /= len(nxt_times)

tohist = []
for key, val in ext_times.items():
  try:
    tohist.append(100*(val/nxt_times[key] - 1.))
  except KeyError:
    pass
tohist = sorted(tohist)

fig, ax = plt.subplots()
plt.xticks(np.arange(0, 240, step=20))
plt.yticks(np.arange(0, 1.1, step=0.1))
plt.grid(b=True, which='major', color='gray', linestyle='-', alpha=0.2)
plt.grid(b=True, which='minor', color='gray', linestyle='-', alpha=0.2)

n_bins = len(tohist)*3

n, bins, patches = plt.hist(tohist, n_bins, density=True, histtype='step',
                           cumulative=True, label='With Modified Adblocker')

plt.legend(loc='lower right')

plt.xlabel('% Overhead for Page Load Time')
plt.ylabel('Fraction of Websites')
plt.title('CDF of % Overhead for AdBlockers') 


axpolygons = [poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)]
for poly in axpolygons:
  poly.set_xy(poly.get_xy()[:-1])

plt.savefig('adblocker_overhead', format='pdf')
plt.show()
