import json
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np



ratio_news = []
ratio_news_1level = []
ratio_ustop200 = []
ratio_ustop200_1level = []

with open('site_network_news_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_news.append(time['ad_plus_inherited_ratio'])

with open('site_network_news_1level_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_news_1level.append(time['ad_plus_inherited_ratio'])

with open('site_network_ustop200_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_ustop200.append(time['ad_plus_inherited_ratio'])

with open('site_network_ustop200_1level_t.json','r') as f:
  stat = json.load(f)
for site, time in stat.items():
  ratio_ustop200_1level.append(time['ad_plus_inherited_ratio'])

n_bins = 10000  
n, bins, patches = plt.hist(ratio_news, n_bins, density=True, histtype='step',
                           cumulative=True, label='News')

n, bins, patches = plt.hist(ratio_news_1level, n_bins, density=True, histtype='step',
                           cumulative=True, label='News_1L')

n, bins, patches = plt.hist(ratio_ustop200, n_bins, density=True, histtype='step',
                           cumulative=True, label='top200')

n, bins, patches = plt.hist(ratio_ustop200_1level, n_bins, density=True, histtype='step',
                           cumulative=True, label='top200_1L')

plt.legend()

plt.xlabel('network cost ratio of ads')
plt.ylabel('Fraction of websites')
plt.title('ads network cost (CDF)') 


plt.savefig('network_cost_cdf', format='pdf')
plt.show()



