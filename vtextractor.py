import json
import requests

TOP_N = 3  #cutoff number for extracting trusted domains
VT_SCORE = 0.0155  #cutoff threshold for extracting trusted domains

def vt_extractor(domain_list):
  url = 'https://www.virustotal.com/vtapi/v2/domain/report'
  scored_domains = []
  for domain in domain_list:
    params = {'apikey':'68471d4ea8fb9e689b547b988f4fe2d5c0de5898cfc41e91ebbe00cdbd8d88cb', 'domain':domain}
    vt_score = 0.0
    try:
      ### extract vt data
      response = requests.get(url, params=params)
      data = response.json()
      ### calculate vt score     
      for item in data['detected_urls']:
        vt_score = vt_score + float(item['positives'])/item['total'] 
      try:
        vt_score = vt_score / len(data['detected_urls'])
      except ZeroDivisionError:
        pass
      ### attach (domain, vt score) to the list
      scored_domains.append((domain, vt_score))
      print "Finished:",domain
    except:
      continue

  ### sort the list
  scored_domains.sort(key=lambda tup: tup[1]) 
  ### print sorted list
  print scored_domains

  ### uncomment one of these two:
  #return [item[0] for item in scored_domains[:TOP_N]]
  #return [item[0] for item in scored_domains if item[1] < VT_SCORE]

if __name__ == "__main__" :
  vt_extractor(['apple.com', 'yahoo.com', 'googlesyndication.com','doubleclick.com', 'bbc.com'])


