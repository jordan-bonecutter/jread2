import json
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np


aggregatedStat_news = {}
with open('cat_stat_news_t.json','r') as f:
  stat = json.load(f)
for cat, time in stat.items():
  if cat == 'js_evaluate':
    cat = 'Scripting'
  if cat == 'js_function':
    cat = 'Scripting'
  if cat == 'html_parse':
    cat = 'HTML Parsing'
  if cat == 'css_parse':
    cat = 'Styling'
  if cat == 'style_recalc':
    cat = 'Styling'
  if cat == 'layout':
    cat = 'Layout'
  if cat == 'update_layer':
    cat = 'Layout'
  if cat == 'paint':
    cat = 'Paint'
  if cat == 'paint_image':
    cat = 'Paint'
  if cat == 'composite':
    cat = 'Composite'
  if cat == 'xhr':
    continue
  if cat in aggregatedStat_news.keys():
    aggregatedStat_news[cat][0] += time[0]
    aggregatedStat_news[cat][1] += time[1]
  else:
    aggregatedStat_news[cat] = time

totalTime = 0.0
adTime = 0.0
for _, time in aggregatedStat_news.items():
  totalTime += time[0]
  adTime += time[1]

label = []
ratio_catAd_to_ads = []
ratio_catTotal_to_total = []
ratio_catAd_to_catTotal = []
for cat, time in aggregatedStat_news.items():
  label.append(cat)
  ratio_catAd_to_ads.append(time[1]/adTime)
  ratio_catTotal_to_total.append(time[0]/totalTime)
  ratio_catAd_to_catTotal.append(time[1]/time[0])



l = np.arange(len(label))
l_catAd_to_catTotal = plt.bar(l-0.2, ratio_catAd_to_catTotal, width=0.2, color='g', align='center')
l_catAd_to_ads = plt.bar(l, ratio_catAd_to_ads, width=0.2, color='b', align='center')
l_catTotal_to_total = plt.bar(l+0.2, ratio_catTotal_to_total, width=0.2, color='r', align='center')
y_pos = range(len(label))
plt.xticks(y_pos, label, rotation=50)
plt.ylabel('Fraction')
plt.title('Contribution of stages in performance cost of ads')
plt.legend( ( l_catAd_to_catTotal[0], l_catAd_to_ads[0], l_catTotal_to_total[0]), ('Ratio of Stage Ad-Workload to Stage Workload', 'Ratio of Stage Ad-Workload to Total Ad-Workload ', 'Ratio of Stage Workload to Total Workload  ') )
plt.tight_layout()
plt.savefig('stage_ratio', format='pdf')
plt.show()
