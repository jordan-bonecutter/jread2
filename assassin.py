import threading
import os
from dbprint import dbprint

tklock = None
tokill = None

def periodic(func):
  def inner(*args, **kwargs):
    func(*args, **kwargs)
    t = threading.Timer(1000, periodic(func))
    t.daemon = True
    t.start()
  return inner

@periodic
def assassinate():
    global tokill, tklock
    dbprint("killing weird chromiums")
    for p in tokill:
        os.system("kill " + str(p)) 
    tklock.acquire()
    tokill = []
    tklock.release()
    os.system("killall Chromium")

