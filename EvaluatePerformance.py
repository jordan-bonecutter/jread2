import copy
from adblockparser import AdblockRules
import json
from json import encoder
from collections import OrderedDict
import filehelper
from dbprint import dbprint

class EvaluatePerformance():

  def __init__(self, reportFile):
    self._reportFile = reportFile
    self.perfEvents = []
    self._event_filter_list = ["ParseAuthorStyleSheet", "EvaluateScript", "ParseHTML", "FunctionCall", "UpdateLayoutTree", "InvalidateLayout", "ScheduleStyleRecalculation", "Layout", "UpdateLayerTree", "Paint", "CompositeLayers"]

  def filter_and_sort_traces(self, trace_data):  ### filter traces. change "X" to "B/E". sort traces by start time 
    filtered_traces = []
    for trace in trace_data:
      if trace["name"] in self._event_filter_list:
        if trace["ph"] == "X":
          filtered_traces.append(trace)
          filtered_traces[-1]["ph"] = "B"
          filtered_traces.append(trace.copy())
          filtered_traces[-1]["ph"] = "E"
          filtered_traces[-1]["ts"] = int(filtered_traces[-1]["ts"])+int(filtered_traces[-1]["dur"])
        else:
          filtered_traces.append(trace)
    return sorted(filtered_traces, key = lambda t:(int(t["pid"]), int(t["tid"]), int(t["ts"])))

  def add_performance(self, website, trace_data, ad_urls):
    B_trace_stack = []   # list of started traces ("ph":"B"). each element is a dict {"name":name_of_event, "start":start_time, "deduct":aggregated_time_on_child_activitis, "url":url_associated_to_trace, "ad":0->non-ad 1->ad
    layoutInvalidate = {}  # {frameId:url} -> url is the url associate to the event triggers InvalidateLayout. 
    lastScheduleRecalcStyle = {}   # {frameId:url} -> url is the url associate to the event triggers ScheduleStyleRecalculation. 
                                   # E.g. it could be url associated with updateLayoutTree that calls ScheduleStyleRecalculation 
                                   # or url of script that triggers ScheduleStyleRecalculation
    lastRecalcStyleInitiator = None # it will fill with (str,int) tuple: (url associate to last UpdateLayoutTree, end time of last UpdateLayoutTree).
                                    # Check https://github.com/ChromeDevTools/devtools-frontend/blob/5a55ae9517a2586e38358962162c638578ca958a/front_end/timeline_model/TimelineModel.js:755
    lastReflowOrLayout = (None, None) # (frameId, URL) assoicated to the last Layout or UpdateLayoutTree. Used to determine initiator of UpdateLayerTree, Paint and CompositeLayers
                                      # will reset after non-reflow activity (any activity except 
                                      # [Layout, UpdateLayoutTree, UpdateLayerTree, Paint, CompositeLayers, UpdateLayer, SetLayerTreeId, ScheduleStyleRecalculation, InvalidateLayout])
    perfEvent = {"website":website, \
                 "activity_time":{ \
                                   "css_parse":[0,0],       \
                                   "js_evaluate":[0,0],     \
                                   "html_parse":[0,0],      \
                                   "js_function":[0,0],     \
                                   "style_recalc":[0,0],    \
                                   "layout":[0,0],	    \
                                   "update_layer":[0,0],    \
                                   "paint":[0,0],	    \
                                   "composite":[0,0]	    \
                                  }}  # 1st element: total time, 2nd element: ad time 

    sorted_filtered_traces = self.filter_and_sort_traces(trace_data)
      
    for trace in sorted_filtered_traces:
      if trace["name"] in ["SetLayerTreeId", "UpdateLayer"]:
        continue
      if trace["name"] == "UpdateLayerTree":
        url = None
        try:
          if trace["args"]["data"]["frame"] == lastReflowOrLayout[0]:
            url = lastReflowOrLayout[1]
        except:
          continue
        self.parse_trace(trace, perfEvent["activity_time"]["update_layer"], B_trace_stack, url, ad_urls)

      if trace["name"] == "Paint":
        url = None
        try:
          if trace["args"]["data"]["frame"] == lastReflowOrLayout[0]:
            url = lastReflowOrLayout[1]
        except:
          continue
        self.parse_trace(trace, perfEvent["activity_time"]["paint"], B_trace_stack, url, ad_urls)

      if trace["name"] == "CompositeLayers":
        url = lastReflowOrLayout[1]
        self.parse_trace(trace, perfEvent["activity_time"]["composite"], B_trace_stack, url, ad_urls)
        
      if trace["name"] == "InvalidateLayout":
        frameId = trace["args"]["data"]["frame"]
        url = None
        if "stackTrace" in trace["args"]["data"].keys():
          url = trace["args"]["data"]["stackTrace"][0]["url"]
        # Check https://github.com/ChromeDevTools/devtools-frontend/blob/5a55ae9517a2586e38358962162c638578ca958a/front_end/timeline_model/TimelineModel.js:755
        elif lastRecalcStyleInitiator != None and (frameId in layoutInvalidate.keys()) and layoutInvalidate[frameId] != None and lastRecalcStyleInitiator[1] < int(trace["ts"]):
            url = lastRecalcStyleInitiator[0]
        elif len(B_trace_stack):
          url = B_trace_stack[-1]["url"]
        layoutInvalidate[frameId] = url

      ### finds url associates to caller of ScheduleStyleRecalculation
      if trace["name"] == "ScheduleStyleRecalculation":
        frameId = trace["args"]["data"]["frame"]
        url = None
        if "stackTrace" in trace["args"]["data"].keys():
          url = trace["args"]["data"]["stackTrace"][0]["url"]
        elif len(B_trace_stack):
          url = B_trace_stack[-1]["url"]
        lastScheduleRecalcStyle[frameId] = url

      if trace["name"] == "ParseAuthorStyleSheet":
        try:
          url = trace["args"]["data"]["styleSheetUrl"]
        except:
          url = None
        self.parse_trace(trace, perfEvent["activity_time"]["css_parse"], B_trace_stack, url, ad_urls)
        ### invalidate reflow
        lastReflowOrLayout = (None, None)
        continue

      if trace["name"] == "EvaluateScript":
        try:
          url = trace["args"]["data"]["url"]
        except:
          url = None
        self.parse_trace(trace, perfEvent["activity_time"]["js_evaluate"], B_trace_stack, url, ad_urls)
        ### invalidate reflow
        lastReflowOrLayout = (None, None)
        continue

      if trace["name"] == "ParseHTML":
        try:
          url = trace["args"]["beginData"]["url"]
        except:
          url = None
        self.parse_trace(trace, perfEvent["activity_time"]["html_parse"], B_trace_stack, url, ad_urls)
        ### invalidate reflow
        lastReflowOrLayout = (None, None)
        continue

      if trace["name"] == "FunctionCall":
        try:
          url = trace["args"]["data"]["url"]
        except:
          url = None
        self.parse_trace(trace, perfEvent["activity_time"]["js_function"], B_trace_stack, url, ad_urls)
        ### invalidate reflow
        lastReflowOrLayout = (None, None)
        continue

      if trace["name"] == "UpdateLayoutTree":
        try:
          url = trace["args"]["beginData"]["stackTrace"][0]["url"]
        except:
          try:
            url = lastScheduleRecalcStyle[trace["args"]["beginData"]["frame"]]
          except:
            url = None
        ### register initiator url and end time for this trace. 
        ### Check https://github.com/ChromeDevTools/devtools-frontend/blob/5a55ae9517a2586e38358962162c638578ca958a/front_end/timeline_model/TimelineModel.js:739
        if trace["ph"] == "E":
          try:
            if B_trace_stack[-1]["name"] == "UpdateLayoutTree":
              lastRecalcStyleInitiator = (B_trace_stack[-1]["url"], int(trace["ts"]))
          except:
            lastRecalcStyleInitiator  = (None, int(trace["ts"]))
        self.parse_trace(trace, perfEvent["activity_time"]["style_recalc"], B_trace_stack, url, ad_urls)
        ### register frameId and url for later reflow activities
        try:
          lastReflowOrLayout = (trace["args"]["beginData"]["frame"], url)
        except:
          pass
        continue

      if trace["name"] == "Layout":
        try:
          url = trace["args"]["beginData"]["stackTrace"][0]["url"]
        except:
          try:
            url = layoutInvalidate[trace["args"]["beginData"]["frame"]]
          except:
            url = None
        ### validate layout
        try:
          layoutInvalidate[trace["args"]["beginData"]["frame"]] = None
        except:
          pass
        self.parse_trace(trace, perfEvent["activity_time"]["layout"], B_trace_stack, url, ad_urls)
        ### register frameId and url for later reflow activities
        try:
          lastReflowOrLayout = (trace["args"]["beginData"]["frame"], url)
        except:
          pass
        continue
    
    self.perfEvents.append(perfEvent)

    #json.dump(perfEvent, self._reportFile, indent=4)  # print

    return

  def print_perfEvents(self):
    if self._reportFile:
      json.dump(self.perfEvents, self._reportFile, indent=4)
    else:
      json.dump(self.perfEvents, indent=4)

  def checkpoint(self, fname):
    filehelper.json_save(self.perfEvents, fname)


  def parse_trace(self, trace, time, B_trace_stack, url, ad_urls):
    name = trace["name"]
    if trace["ph"] == "B":
      ### check for ad and push to the B_trace_stack           
      try:
        if url in ad_urls:
          B_trace_stack.append({"name":trace["name"], "start":int(trace["ts"]), "deduct":0, "url":url, "ad":1})
        else:
          B_trace_stack.append({"name":trace["name"], "start":int(trace["ts"]), "deduct":0, "url":url, "ad":0})
      except:
        dbprint( "WARNING: cannot relate ", name, " to url")
        pass
    else:  # ph:"E"
      try:
        B_event = B_trace_stack.pop()
      except:  #some trace file start from E activity. FIXME
        dbprint("WARNING: missing start trace for an activity") 
        return
      ### check mismatch in B/E FIXME
      if B_event["name"] != name:
        dbprint( "WARNING: found missmatch in "+ name + " begin and end")
        B_trace_stack.append(B_event)
      else:
        act_dur = int(trace["ts"]) - B_event["start"] - B_event["deduct"]
        time[0] += act_dur
        if B_event["ad"] == 1:  #check for ad
          time[1] += act_dur
        ### add duration to the parent activity (to be "deducted" later)
        try:
          B_trace_stack[-1]["deduct"] += (act_dur+B_event["deduct"])
        except:
          pass
    return