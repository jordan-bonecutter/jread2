# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# snapfile.py # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter # # # # # # # # # # # # # # # # # #
# copyright - all rights reserved # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
from typing import IO

class FileNotReadyError(RuntimeError):
    def __init__(self):
        pass

class SnapFile:
    _fd       = None
    _fname    = None
    _contents = None

    def __init__(self, fd):
        self._fd = fd
        self._fname = fd.name

    @classmethod
    def open(cls, fname) -> object:
        return cls(open(fname, "w"))

    def close(self):
        if self._fd is not None:
            self._fd.close()
            with open(self._fname, "r") as fi:
                self._contents = fi.read()
            os.remove(self._fname)
            self._fd = None

    @property
    def contents(self) -> str:
        if self._fd is not None:
            raise FileNotReadyError()
        else:
            return self._contents

    @property
    def fd(self) -> IO:
        return self._fd
