#!/usr/bin/env python3

# ABOUT THIS MODULE
# This module provides basic functionality for handling a log file.
# It is solely used by master.py and more information can be found there.
#
# The log is composed chronologically, new information is simply appended
# at the bottom of the file.

import os
from filehandler import *

class LogFile:
    def __init__(self, name, persistence):
        pass

    def append(self, *args):
        pass

    def truncate(self, persistent):
        pass
