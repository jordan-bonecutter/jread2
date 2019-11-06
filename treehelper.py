# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# treehelper.py # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import tldextract
import requests
from adblockparser import AdblockRules
import json
import os
try:
  import _pickle as pickle
except:
  import pickle
import filehelper
import re
from typing import List, Dict, Union, Any

_rules = None
_rules_pkl = "pickles/rules.pkl"
_rules_file = "setup_files/easylist.json"

_vt_attr = None
_vt_apkf = "setup_files/vt.key"
_vt_pkl = "pickles/vt.pkl"

name_limit = 30000


Node = Dict[str, Union[Dict[str, int], str, int]]
Level = List[Node]
Tree = List[Level]
Recursive = None
ZBTree = Dict[str, Union[List[Recursive], Dict[str, str]]]


def num_ad_nodes(tree: Tree, explicit: bool) -> int:
    ret = 0
    for layer in tree:
        for url, data in layer.items():
            if explicit:
                if data["ad"] == "yes":
                    ret += 1
            else:
                if data["ad"] != "no":
                    ret += 1
    return ret

def num_nodes(tree: Tree) -> int:
    ret = 0
    for layer in tree:
        ret += len(layer)
    return ret

def get_url(url: str) -> str:
    if url == None:
        return "nil"

    # use tldextract to get the domain
    ext = tldextract.extract(url)

    # if it couldn't find anything
    if ext.domain == "" or ext.suffix == "":
        return url
    else:
        if ext.subdomain != 'www' and ext.subdomain != '':
            return '.'.join((ext.subdomain, ext.domain, ext.suffix))
        return ".".join((ext.domain, ext.suffix))

def _get_vtscore(url: str) -> Dict[str, str]:
    return None
    global _vt_attr

    if _vt_attr == None:
        if os.path.exists(_vt_pkl):
            with open(_vt_pkl, "rb") as fi:
                _vt_attr = pickle.load(fi)
        else:
            _vt_attr = {"req_url": "https://www.virustotal.com/vtapi/v2/url/report", "hist":{}}

    if not "apk" in _vt_attr:
        with open(_vt_apkf, "r") as fi:
            _vt_attr.update({"apk": fi.read()})
    if not "params" in _vt_attr:
        _vt_attr.update({"params": {"apikey": _vt_attr["apk"], "resource": None}})

    try:
        return _vt_attr["hist"][url]

    except KeyError:
        _vt_attr["params"]["resource"] = url

        response = requests.get(_vt_attr["req_url"], params=_vt_attr["params"])
        try:
            js = response.json()
            _vt_attr["hist"].update({url: js})
            return js
        except (json.decoder.JSONDecodeError, KeyError):
            return 0


def get_raw_depth(rtree: ZBTree) -> int:
    return _get_raw_depth(rtree["_root"], 1)


def _get_raw_depth(rtree: ZBTree, depth: int) -> int:
    if not "children" in rtree:
        return depth
    
    mdepth = depth
    for child in rtree["children"]:
        mdepth = max(_get_raw_depth(child, depth+1), mdepth)

    return mdepth


def get_tree(rtree: ZBTree, performance: Any) -> Tree:
    global _rules
    if _rules == None:
        if os.path.exists(_rules_pkl):
            with open(_rules_pkl, "rb") as fi:
                _rules = pickle.load(fi)
        else:
            with open(_rules_file, "r") as fi:
                _rules = AdblockRules(json.loads(fi.read()))
            filehelper.file_save(_rules, _rules_pkl, pickle.dump, True)

    # set variables
    tree = []

    traverse_tree(rtree["_root"], tree, performance, 0)

    for idl, layer in enumerate(tree[1:]):
        for url, node in layer.items():
            if node["ad"] == "yes":
                continue
            for parent in node["parents"].keys():
                if tree[idl][parent]["ad"] != "no":
                    node["ad"] = "inherited"
                    break

    return {"tree_full": tree, "tree_trim": _trim_tree(tree)}


def traverse_tree(rtree: ZBTree, tree: Tree, performance: Any, layer: int):
    global _rules

    # ensure tree is big enough
    if len(tree) is layer:
        tree.append({})

    # get node name and parent name
    nname = str(rtree["data"])[:name_limit]
    pname = str(rtree["parent"])[:name_limit]
    if nname in tree[layer]:
        try:
            tree[layer][nname]["parents"][pname] += 1
        except KeyError:
            tree[layer][nname]["parents"].update({pname: 1})

    # if the child is not in the tree
    else:
        tree[layer].update({nname: {"parents": {pname: 1}, "vt": None, "type": None, "ad": None, "f_id":None}})

        # set vtscore
        vtres = _get_vtscore(nname)
        tree[layer][nname]["vt"] = {"positives": None, "total": None}
        try:
            tree[layer][nname]["vt"]["positives"] = vtres["positives"]
            tree[layer][nname]["vt"]["total"] = vtres["total"]
        except (KeyError, TypeError):
            pass

        # set ad state
        if _rules.should_block(nname):
            tree[layer][nname]["ad"] = "yes"
        else:
            tree[layer][nname]["ad"] = "no"

        # set content type
        try:
            tree[layer][nname]["resptype"]=rtree["networkData"]["response"]["response"]["headers"]["content-type"]
        except KeyError:
            tree[layer][nname]["resptype"]="unknown"
        try:
            tree[layer][nname]["reqtype"] = rtree["networkData"]["request"]["type"]
        except KeyError:
            tree[layer][nname]["reqtype"] = "unknown"

        # set frameId
        try: 
            tree[layer][nname]["f_id"] = rtree["networkData"]["request"]["frameId"]
        except KeyError:
            pass

        try:
            tree[layer][nname]["reqId"] = rtree["networkData"]["request"]["requestId"]
        except KeyError:
            try:
                tree[layer][nname]["reqId"] = rtree["networkData"]["response"]["requestId"]
            except KeyError:
                pass

        try:
            tree[layer][nname]["timing"] = rtree["networkData"]["response"]["timestamp"]-rtree["networkData"]["request"]["timestamp"]
        except KeyError:
            pass

    if not "children" in rtree:
        return

    for child in rtree["children"]:
        traverse_tree(child, tree, performance, layer+1)


def _trim_tree(tree: Tree) -> Tree:
    trim = []
    for idl, level in enumerate(tree):
        trim.append({})
        for name, info in level.items():
            alias = get_url(name)
            try:
                trim[idl][alias]["squish"] += 1
                try:
                    trim[idl][alias]["types"][info["type"]] += 1
                except KeyError:
                    trim[idl][alias]["types"].update({info["type"]: 1})
                if trim[idl][alias]["ad"] == "no" and info["ad"] != "no":
                    trim[idl][alias]["ad"] = info["ad"]
                elif trim[idl][alias]["ad"] != "yes" and info["ad"] == "yes":
                    trim[idl][alias]["ad"] = "yes"
            except KeyError:
                trim[idl].update({alias: {"parents": {}, "ad": "no", "squish": 1, "vt": 0, "types": {}}})
                trim[idl][alias]["vt"] = info["vt"]
                try:
                    trim[idl][alias]["types"][info["type"]] += 1
                except KeyError:
                    trim[idl][alias]["types"].update({info["type"]: 1})
                trim[idl][alias]["ad"] = info["ad"]
            for parent in info["parents"]:
                palias = get_url(parent)
                try:
                    trim[idl][alias]["parents"][palias] += 1
                except KeyError:
                    trim[idl][alias]["parents"].update({palias: 1})

    for idl, layer in enumerate(trim[1:]):
        for url, node in layer.items():
            if node["ad"] == "yes":
                continue
            for parent in node["parents"].keys():
                if trim[idl][parent]["ad"] != "no":
                    node["ad"] = "inherited"
                    break

    return trim
