#!/usr/bin/env python3

# ABOUT THIS MODULE
# This module provides basic functionality for handling a log file.
# It is solely used by master.py and more information can be found there.
#
# The log is composed chronologically, new information is simply appended
# at the bottom of the file.

import os

class LogFile:
    def __init__(self, name, header, persistence):
        self.name = name
        self.header = header
        self.persistence = persistence

    def append(self, string):
        '''Appends an arbitrary string to the end of the file.'''
        try:
            log = open(self.name, 'a')
            log.write('\n' + string)
            log.close()
        except Exception as exception:
            print('E: loghandler.py: append(): {} exception occurred!'.format(type(exception).__name__))

    def append_header(self, below = ''):
        '''This appends a header to an entry. These headers must be unique enough to allow incremental search of entries.
        
        The below parameter is an optional string that will be appended after the header and a newline.
        '''
        try:
            f = open(self.name, 'a')
            f.write('\n{}\n{}\n'.format(self.header, below))
            f.close()
        except Exception as exception:
            print('E: loghandler.py: append_header(): {} exception occurred!'.format(type(exception).__name__)


    def truncate(self):
        '''Truncates the log file, so that it doesn't grow too big in size, as denoted by the self.persistence variable'''
        try:
            f = open(self.name, 'r')
            lines = f.readlines()
            f.close()
            entries = []
            for i in range(len(lines)):
                if lines[i][:len(self.header)] == self.header:
                    entries.append(i)
            overflow = len(entries) - self.persistence
            if overflow > 0:
                lines = lines[entries[overflow]:]
                f = open(self.name, 'w')
                for line in lines:
                    f.write(line)
                f.close()
        except Exception as exception:
            print('E: loghandler.py: truncate(): {} exception occurred when opening {}!'.format(type(exception).__name__, self.name))

