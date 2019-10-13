import json
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np

def get_time(word):
  return float( word.split()[1].split("m")[0])
def get_request(word):
  return int(word.split(":")[1])

with open('nxt_info8.json','r') as f:
  vanilla = json.load(f)
with open('ext_info8.json','r') as f:
  blocking = json.load(f)

x = []
y = []

vanillaStat = {}
for site in vanilla.keys():
  time = 0.0
  requests = 0
  n = 0
  for item in vanilla[site]:
    if item.find("load") >= 0:
      time += get_time(item)
      n += 1  
    elif item.find("request") >= 0:
      requests += get_request(item)
  if n :
    #print (time/n, float(requests)/n)
    vanillaStat[site] = {'time':time/n, 'requests':float(requests)/n}
blockingStat = {}
for site in blocking.keys():
  time = 0.0
  requests = 0
  n = 0
  for item in blocking[site] :
    if item.find("load") >= 0:
      time += get_time(item)
      n += 1  
    elif item.find("request") >= 0:
      requests += get_request(item)
  if n :
    #print (time/n, float(requests)/n)
    blockingStat[site] = {'time':time/n, 'requests':float(requests)/n}

for site in vanillaStat.keys():
  if site in blockingStat.keys():
    y.append((blockingStat[site]['time'] - vanillaStat[site]['time'])/blockingStat[site]['time'])
    x.append(vanillaStat[site]['requests'])

#x = np.linspace(0, 10, 30)
#y = np.sin(x)

plt.plot(x, y, 'o', color='black')
plt.show()



