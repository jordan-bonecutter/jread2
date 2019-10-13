import json
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np




aggregatedStat_news = {}
with open('contentType_number_news.json','r') as f:
  stat = json.load(f)
for ctype, number in stat.items():
  if ctype == 'Fetch':
    ctype = 'XHR'
  if ctype == 'Other':
    ctype = 'unknown'
  if ctype == 'Document':
    ctype = 'HTML'
  if ctype in aggregatedStat_news.keys():
    aggregatedStat_news[ctype]['total'] += number['total']
    aggregatedStat_news[ctype]['ad'] += number['ad']
    aggregatedStat_news[ctype]['ad_plus_inherited'] += number['ad_plus_inherited']
  else:
    aggregatedStat_news[ctype] = number

aggregatedStat_news_1level = {}
with open('contentType_number_news_1level.json','r') as f:
  stat = json.load(f)
for ctype, number in stat.items():
  if ctype == 'Fetch':
    ctype = 'XHR'
  if ctype == 'Other':
    ctype = 'unknown'
  if ctype == 'Document':
    ctype = 'HTML'
  if ctype in aggregatedStat_news_1level.keys():
    aggregatedStat_news_1level[ctype]['total'] += number['total']
    aggregatedStat_news_1level[ctype]['ad'] += number['ad']
    aggregatedStat_news_1level[ctype]['ad_plus_inherited'] += number['ad_plus_inherited']
  else:
    aggregatedStat_news_1level[ctype] = number

aggregatedStat_ustop200 = {}
with open('contentType_number_ustop200.json','r') as f:
  stat = json.load(f)
for ctype, number in stat.items():
  if ctype == 'Fetch':
    ctype = 'XHR'
  if ctype == 'Other':
    ctype = 'unknown'
  if ctype == 'Document':
    ctype = 'HTML'
  if ctype in aggregatedStat_ustop200.keys():
    aggregatedStat_ustop200[ctype]['total'] += number['total']
    aggregatedStat_ustop200[ctype]['ad'] += number['ad']
    aggregatedStat_ustop200[ctype]['ad_plus_inherited'] += number['ad_plus_inherited']
  else:
    aggregatedStat_ustop200[ctype] = number

aggregatedStat_ustop200_1level = {}
with open('contentType_number_ustop200_1level.json','r') as f:
  stat = json.load(f)
for ctype, number in stat.items():
  if ctype == 'Fetch':
    ctype = 'XHR'
  if ctype == 'Other':
    ctype = 'unknown'
  if ctype == 'Document':
    ctype = 'HTML'
  if ctype in aggregatedStat_ustop200_1level.keys():
    aggregatedStat_ustop200_1level[ctype]['total'] += number['total']
    aggregatedStat_ustop200_1level[ctype]['ad'] += number['ad']
    aggregatedStat_ustop200_1level[ctype]['ad_plus_inherited'] += number['ad_plus_inherited']
  else:
    aggregatedStat_ustop200_1level[ctype] = number

val_news = []
val_news_1level = []
val_ustop200 = []
val_ustop200_1level = []
val_news_ad = []
val_news_1level_ad = []
val_ustop200_ad = []
val_ustop200_1level_ad = []
label =[]


for ctype in aggregatedStat_news.keys():
  val_news.append(aggregatedStat_news[ctype]['total'])
  val_news_1level.append(aggregatedStat_news_1level[ctype]['total'])
  val_ustop200.append(aggregatedStat_ustop200[ctype]['total'])
  val_ustop200_1level.append(aggregatedStat_ustop200_1level[ctype]['total'])
  val_news_ad.append(aggregatedStat_news[ctype]['ad'])
  val_news_1level_ad.append(aggregatedStat_news_1level[ctype]['ad'])
  val_ustop200_ad.append(aggregatedStat_ustop200[ctype]['ad'])
  val_ustop200_1level_ad.append(aggregatedStat_ustop200_1level[ctype]['ad'])
  label.append(ctype)

l = np.arange(len(label))

l_news = plt.bar(l-0.3, val_news, width=0.2, color='b', align='center')
l_news_ad = plt.bar(l-0.3, val_news_ad, bottom = val_news, width=0.2, color='c', align='center')
l_news_1level = plt.bar(l-0.1, val_news_1level, width=0.2, color='r', align='center')
l_news_1level_ad = plt.bar(l-0.1, val_news_1level_ad, bottom = val_news_1level, width=0.2, color='c', align='center')
l_ustop200 = plt.bar(l+0.1, val_ustop200, width=0.2, color='g', align='center')
l_ustop200_ad = plt.bar(l+0.1, val_ustop200_ad, bottom = val_ustop200, width=0.2, color='c', align='center')
l_ustop200_1level = plt.bar(l+0.3, val_ustop200_1level, width=0.2, color='y', align='center')
l_ustop200_1level_ad = plt.bar(l+0.3, val_ustop200_1level_ad, bottom = val_ustop200_1level, width=0.2, color='c', align='center')
y_pos = range(len(label))
plt.xticks(y_pos, label, rotation=30)
plt.ylabel('number of resources')
plt.legend( (l_news[0], l_news_1level[0], l_ustop200[0], l_ustop200_1level[0] ), ('news', 'news_1level', 'top', 'top_1level') )



n_bins = 50  
#n, bins, patches = plt.hist(x, n_bins, density=True, histtype='step', cumulative=True, label='Empirical')

plt.show()



