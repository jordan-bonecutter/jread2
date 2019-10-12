#
#
#
#

types = ['Stylesheet', 'Image', 'EventSource', 'XHR', 'Document', 'Font', 'Script', 'Other', 'Media', 'Fetch', 'unknown']


def nodetype(node) -> str:
  resptype = node['resptype']
  reqtype  = node['reqtype']

  ret = None

  if resptype == 'unknown' or 'octet' in resptype:
    ret = reqtype
    return ret

  if 'image' in resptype:
    return 'Image'
  elif 'font' in resptype:
    return 'Font'
  elif 'video' in resptype or 'mp4' in resptype:
    return 'Media'
  elif 'html' in resptype:
    return 'HTML'
  elif 'css' in resptype:
    return 'Stylesheet'
  elif 'xml' in resptype:
    return 'XML'
  elif 'javascript' in resptype or 'ecmascript':
    return 'Script'  
  else:
    return resptype+reqtype
