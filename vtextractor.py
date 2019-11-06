import json
import requests
from pprint import pprint

TOP_N = 3  #cutoff number for extracting trusted domains
VT_SCORE = 0.0155  #cutoff threshold for extracting trusted domains

def vt_extractor(domain_list):
  url = 'https://www.virustotal.com/vtapi/v2/domain/report'
  scored_domains = {}
  for domain in domain_list:
    params = {'apikey':'68471d4ea8fb9e689b547b988f4fe2d5c0de5898cfc41e91ebbe00cdbd8d88cb', 'domain':domain}
    vt_score = 0.0
    try:
      ### extract vt data
      response = requests.get(url, params=params)
      data = response.json()
      denom = 0

      ### calculate vt score     
      if 'detected_urls' in data:
        denom += len(data['detected_urls'])
        for item in data['detected_urls']:
          if item['total'] == 0:
            continue
          vt_score = vt_score + float(item['positives'])/item['total'] 

      if 'undetected_urls' in data:
        denom += len(data['undetected_urls'])
        for item in data['undetected_urls']:
          if item[3] == 0:
            continue
          vt_score += float(item[2]/item[3])

      if 'undetected_referrer_samples' in data:
        denom += len(data['undetected_referrer_samples'])
        for item in data['undetected_referrer_samples']:
          if item['total'] == 0:
            continue
          vt_score += float(item['positives']/item['total'])

      if 'undetected_downloaded_samples' in data:
        denom += len(data['undetected_downloaded_samples'])
        for item in data['undetected_downloaded_samples']:
          if item['total'] == 0:
            continue
          vt_score += float(item['positives']/item['total'])

      if 'detected_referrer_samples' in data:
        denom += len(data['detected_referrer_samples'])
        for item in data['detected_referrer_samples']:
          if item['total'] == 0:
            continue
          vt_score += float(item['positives']/item['total'])

      if 'detected_downloaded_samples' in data:
        denom += len(data['detected_downloaded_samples'])
        for item in data['detected_downloaded_samples']:
          if item['total'] == 0:
            continue
          vt_score += float(item['positives']/item['total'])

      try:
        vt_score = vt_score / denom 
      except ZeroDivisionError:
        print('ZDE')
        vt_score = -1
        pass
      ### attach (domain, vt score) to the list
      scored_domains[domain] = {'raw_score': vt_score}
      try:
        scored_domains[domain]['alexa_cat'] = data['Alexa category']
      except KeyError:
        pass
      try:
        scored_domains[domain]['wot']       = data['WOT domain info']
      except KeyError:
        pass
      try:
        scored_domains[domain]['webutation'] = data['Webutation domain info']
      except KeyError:
        pass
      print( "Finished:", domain, vt_score)
    except Exception as e:
      print(e)
      continue

  ### sort the list
  #scored_domains.sort(key=lambda tup: tup[1]) 
  ### print sorted list
  #print scored_domains

  ### uncomment one of these two:
  #return [item[0] for item in scored_domains[:TOP_N]]
  #return [item[0] for item in scored_domains if item[1] < VT_SCORE]
  return scored_domains

if __name__ == "__main__" :
  with open('addomains_dict.json', 'r') as fi:
    sites = list(json.load(fi).keys())
  with open('vtout.json', 'w') as fi:
    json.dump(vt_extractor(sites), fi)
