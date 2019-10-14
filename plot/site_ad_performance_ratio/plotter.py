import numpy as np
import json
import matplotlib as mpl
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np

ratio_news = []
ratio_news_1level = []
ratio_ustop200 = []
ratio_ustop200_1level = []


with open('site_stat_news_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_news.append(time['ratio'])

with open('site_stat_news_1level_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_news_1level.append(time['ratio'])

with open('site_stat_ustop200_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_ustop200.append(time['ratio'])

with open('site_stat_ustop200_1level_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_ustop200_1level.append(time['ratio'])

fig, ax = plt.subplots()
plt.xticks(np.arange(0, 1.1, step=0.1))
plt.yticks(np.arange(0, 1.1, step=0.1))
plt.grid(b=True, which='major', color='gray', linestyle='-', alpha=0.2)
plt.grid(b=True, which='minor', color='gray', linestyle='-', alpha=0.2)

n_bins = 10000
n, bins, patches = plt.hist(ratio_news, n_bins, density=True, histtype='step',
                           cumulative=True, label='News (landing)', range=(0., 1.))

n, bins, patches = plt.hist(ratio_news_1level, n_bins, density=True, histtype='step',
                           cumulative=True, label='News (post-click)', range=(0., 1.))

n, bins, patches = plt.hist(ratio_ustop200, n_bins, density=True, histtype='step',
                           cumulative=True, label='General (landing)', range=(0., 1.))

n, bins, patches = plt.hist(ratio_ustop200_1level, n_bins, density=True, histtype='step',
                           cumulative=True, label='General (post-click)', range=(0., 1.))

plt.legend(loc='lower right')

plt.xlabel('Computation Cost Ratio of Ads')
plt.ylabel('Fraction of Websites')
plt.title('Ads Computation Cost (CDF)') 


axpolygons = [poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)]
for poly in axpolygons:
  poly.set_xy(poly.get_xy()[:-1])

plt.savefig('computation_cost_cdf', format='pdf')
plt.show()
