# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# kbinterruptable.py  # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from dbprint import dbprint
from typing import Callable, Any

def kbint(func: Callable, cleanup: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            dbprint("cleaning up")
            cleanup()
        raise KeyboardInterrupt()
    return inner
