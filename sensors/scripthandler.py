#!/usr/bin/env python3

import re
import os

class Script:
    def __init__(self, name, args, command='python', logfile='sensors.log'):
        self.name    = name
        self.args    = args
        self.command = command
        self.logfile = logfile
        
    def call(self):
        cmd = self.concat_callable()
        try:
            output = os.system(cmd)
        except Exception as exception:
            print('E: scripthandler.py: Exception occurred for \'{}\': \'{}\'. Reading failed.'.format(cmd, type(exception).__name__))
            return -1
        return output

    def concat_callable(self):
        return '{} {} {} >> {}'.format(self.command, self.name, self.args, self.logfile)
        
    def __repr__(self):
        return """
{}(
script: {},
  exec: {},
   cmd: {}
)
""".format(re.search(r'/([^/]*)$', self.name).group(1), self.command, self.name, self.args, self.concat_callable())

