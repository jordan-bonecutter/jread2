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

for domain, ratio in topDomains:
  label.append(domain)
  val.append(ratio['ratio_to_ads'])

#print (sortedDomain)

l = np.arange(len(label))
plt.bar(l, val, color='darkgrey')
y_pos = range(len(label))
plt.xticks(y_pos, label, fontsize=8, rotation=50, ha='right')
plt.ylabel('Fraction')
plt.title('Contribution of ad domains in performance cost')
plt.tight_layout()
plt.savefig('domain_contribution', format='pdf')
plt.show()



