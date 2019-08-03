#
#
#
#

def get_list_items(json, level):
  curlycount = 0
  strstate   = False
  prev       = None
  curr       = None
  ret        = []
  bstart     = 0
  for idc, char in enumerate(json): 
    prev = curr
    curr = char

    if curr is "\"" and prev is not "\\":
      strstate = not strstate

    elif curr is "{" and not strstate:
      curlycount += 1

    elif curr is "}" and not strstate:
      curlycount -= 1
      if curlycount is level:
        ret.append(json[bstart + 1:idc + 1])
        bstart = idc + 1

  return ret
