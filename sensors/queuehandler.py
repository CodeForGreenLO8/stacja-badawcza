#!/usr/bin/env python3

# ABOUT THIS MODULE
# This module provides basic functionality for handling a queue file.
# It is solely used by master.py and more information can be found there.
#
# The queue follows the LIFO model, because it's more important to first send
# recent information to the server, since it matters more to the end-user.
# 
# The created file stores the most relevant lines on top, in other words,
# since it's LIFO, new values get prepended on top of the file. This is to make
# reading the queue easier.

import os
from filehandler import *

class QueueFile:
    def __init__(self, name):
        self.name = name

    def push(self, *args):
        queue = open(QUEUE_FILE, 'a')
        queue.write()
        queue.close() 

    def top(self):
        queue = open(QUEUE_FILE, 'r')
        line = queue.readline()
        queue.close() 
        return line

    def pop(self):
        queue = open(self.name, 'r')
        lines = queue.readlines()[1:]
        queue.close()
        queue = open(self.name, 'w')
        queue.writelines(lines)
        queue.close()
