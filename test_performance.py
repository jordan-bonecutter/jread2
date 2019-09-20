import os
import re
import fnmatch
import sys
import argparse
import copy
from dbprint import dbprint
from adblockparser import AdblockRules
import json
from json import encoder
from collections import OrderedDict
from EvaluatePerformance import EvaluatePerformance


def extract_ads_rules(infile):
  raw_rules = []    
  raw_rules = infile.readlines()
  return AdblockRules(raw_rules)

def get_ad_urls_from_har(har_file, rules):  ### read HAR file and extract ad urls   
  har_data = json.load(har_file, object_pairs_hook=OrderedDict)
  request_urls = [ (r["request"]["url"], rules.should_block(r["request"]["url"])) for r in har_data["log"]["entries"]]
  ad_urls = [url for url,ad in request_urls if ad]
  dbprint(str(len(request_urls))+" "+ str(len(ad_urls)))
  return ad_urls

def get_traces_from_file(trace_file):
  try:
    trace_data = json.load(trace_file, object_pairs_hook=OrderedDict)
  except json.decoder.JSONDecodeError: #FIXME it is seen missing "]" at the end Zbrowse trace output file
    trace_file.write("]")
    trace_file.seek(0)
    try:
      trace_data = json.load(trace_file, object_pairs_hook=OrderedDict)
    except:
      raise Exception("ERROR encoding json file. Added extra ""]"" to the end of file")
  except:
    raise Exception("ERROR encoding json file")
  if isinstance(trace_data, dict):
    trace_data = trace_data['traceEvents']
  return trace_data	

def parseArg():
  filter_dir_path,_ = os.path.split(os.path.realpath(__file__))
  curr_dir = os.getcwd()
  parser = argparse.ArgumentParser()
  parser.add_argument('--trace-dir','-d',  help='Path to the directory of trace files.', type=str, required= True)
  parser.add_argument('--file', '-f', help='file name or wildcare for traces', type=str, required = True)
  parser.add_argument('--har-dir',  help='Path to the directory of har files.', type=str, required= True)
  parser.add_argument('--filter-dir', help='Path to the directory of filters.', type=str, default=filter_dir_path)
  parser.add_argument('--filter', help='filter file containing rules', type=str, default = "EasyList.txt")
  parser.add_argument('--log-dir', help='path to the directory of log (output and report)', type=str, default=curr_dir)
  parser.add_argument('--report-to-file', help='if it should generate report file', type=str)
  args = parser.parse_args()

  input_files = []
  if args.file.find("*") >= 0:
    for f in os.listdir(args.trace_dir):
      if fnmatch.fnmatch(f,args.file):
        try:
          input_files.append((open(os.path.join(args.trace_dir , f), "r+"),open(os.path.join(args.har_dir , f), "r+")))
        except:
          raise Exception("ERROR: cannot open " + os.path.join(args.trace_dir , f) + " or " + os.path.join(args.trace_dir , f) + " in wildcard.")      
  else:
     try:
       input_files.append((open(os.path.join(args.trace_dir , args.file), "rU"),open(os.path.join(args.har_dir , args.file), "rU")))
     except:
       raise Exception("ERROR: opening file " + os.path.join(args.trace_dir , args.file) + " or " + os.path.join(args.har_dir , args.file))

  if (len(input_files) == 0):
    raise Exception("ERROR: at least one file should be given")

  reportFile = None
  if args.report_to_file:
    reportFile = open(os.path.join(args.log_dir, args.report_to_file),"w+")

  filterFileName = args.filter
  filterFilePath = os.path.join(args.filter_dir, args.filter)
  try:
    filterFile = open(filterFilePath)
  except:
   raise Exception("ERROR: cannot open filter file")

  return input_files, reportFile, filterFile


def test():
  input_files, reportFile, filterFile = parseArg() 
  rules = extract_ads_rules(filterFile)
  perf = EvaluatePerformance(reportFile) 
  for trace_file, har_file in input_files[:]:
    ad_urls = get_ad_urls_from_har(har_file, rules)
    trace_data = get_traces_from_file(trace_file)
    website = trace_file.name.split("/")[-1]
    perf.add_performance(website, trace_data, ad_urls)
  perf.print_perfEvents() 
  return
       
if __name__ == "__main__" :
  test()
