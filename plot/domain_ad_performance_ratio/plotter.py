import json
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np




with open('domain_stat_news_t.json','r') as f:
  stat = json.load(f)

sortedDomain = sorted(stat.items(), key=lambda x: x[1]['ratio_to_ads'], reverse=True)



topDomains = sortedDomain[0:10]

label = []
val = []
pop = []
for domain, ratio in topDomains:
  label.append(domain)
  val.append(ratio['ratio_to_ads'])
  pop.append(stat[domain]['number_of_websites'])

#print (sortedDomain)

l = np.arange(len(label))
bar = plt.bar(l, val, color='darkgrey')
for i, rect in enumerate(bar):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % pop[i], ha='center', va='bottom')

y_pos = range(len(label))
plt.xticks(y_pos, label, fontsize=8, rotation=50, ha='right')
plt.ylabel('Ratio')
plt.ylim([0,0.25])
plt.title('Contribution of ad domains to performance cost')
plt.tight_layout()
plt.savefig('domain_contribution', format='pdf')
plt.show()



