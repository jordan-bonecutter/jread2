# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# dbprint.py  # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import datetime

should_print = True

def dbprint(stuff):
    if not should_print:
        return
    time = str(datetime.datetime.now())
    caller = str(sys._getframe().f_back.f_code.co_name)
    print("[" + caller + " - " + time + "] " + str(stuff))
