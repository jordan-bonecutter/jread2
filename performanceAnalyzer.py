import copy
from adblockparser import AdblockRules
import json
from json import encoder
from collections import OrderedDict
import filehelper
import os
from dbprint import dbprint
from EvaluatePerformance import EvaluatePerformance
from treehelper import get_url

def parsePerformanceTraces(perf, trace_dir, zbrowse_filename): 
  zbrowse_file = open(zbrowse_filename)
  zbrowse_data = json.load(zbrowse_file)
  counter = 0
  for domain, val in zbrowse_data.items():
    snapshots = val['snapshots']
    for l in range(len(snapshots)):
      tree_full = snapshots[l]['tree_full']
      ad_urls = []
      for level in tree_full:
        for url,node in level.items():
          if node["ad"] != "no":
            ad_urls.append(url)
      try:
        domain = get_url(domain)
        trace_path = os.path.join(trace_dir, domain + "_" +str(l+1))
        trace_file = open(trace_path, 'r+')
        trace_data = json.load(trace_file, object_pairs_hook=OrderedDict)
      except json.decoder.JSONDecodeError: #FIXME it is seen missing "]" at the end Zbrowse trace output file
        try:  
          trace_file.write("]")
          trace_file.seek(0)
          trace_data = json.load(trace_file, object_pairs_hook=OrderedDict)
        except:
          dbprint("ERROR encoding json file. Added extra ""]"" to the end of file")
          continue
      except:
        dbprint("WARNING: cannot open file " + domain + "_" + str(l+1) + ". skip this file!")
        continue
      trace_file.close()
      if isinstance(trace_data, dict):
        trace_data = trace_data['traceEvents']
      perf.add_performance(domain, trace_data, ad_urls)
      counter += 1
      if not counter % 50:
        dbprint (str(counter)+ " trace files have been added")

def test():
  perf = EvaluatePerformance()
  #parsePerformanceTraces(perf, './trace_top200', './res/crawl_top200.json')
  #perf.print_perfEvents('perf_top200.log')
  perf.read_perfEvents_from_file('perf.log')
  perf.calculateAdPerformance(True)  
  perf.calculateAdPerformanceByDomain(True)
  perf.calculateAdPerformanceByCategory(True)

if __name__ == "__main__" :
  test()
