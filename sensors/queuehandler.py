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
        try:
            queue = open(self.name, 'r')
            lines = queue.readlines()
            queue.close() 
            lines.insert(0, ' '.join(*args))
            queue = open(self.name, 'w')
            queue.writelines(lines)
            queue.close()
        except Exception as exception:
            print('E: queuehandler.py: push(): An exception occurred: {}'.format(type(exception).__name__))

    def top(self):
        try:
            queue = open(self.name, 'r')
            line = queue.readline()
            queue.close() 
            return line
        except Exception as exception:
            print('E: queuehandler.py: push(): An exception occurred: {}'.format(type(exception).__name__))
            return None

    def pop(self):
        try:
            queue = open(self.name, 'r')
            lines = queue.readlines()
            queue.close()
            if len(lines) == 1:
                file_delete(self.name)
            else:
                lines = lines[1:]
                queue = open(self.name, 'w')
                queue.writelines(lines)
                queue.close()
        except Exception as exception:
            print('E: queuehandler.py: pop(): An exception occurred: {}'.format(type(exception).__name__))

    
    def empty(self):
        return file_exists(self.name)
