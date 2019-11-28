#!/usr/bin/env python3

import re
import os

class Script:
    def __init__(self, name, args, command='python'):
        self.name    = name
        self.args    = args
        self.command = command
        
    def call(self):
        cmd = self.concat_callable()
        try:
            output = os.system(cmd)
        except Exception as exception:
            print('E: scripthandler.py: Exception occurred for \'{}\': \'{}\'. Reading failed.'.format(cmd, type(exception).__name__))
            return -1
        return output

    def concat_callable(self):
        return '{} {} {}'.format(self.command, self.name, self.args)
        
    def shortname(self):
        return re.search(r'/([^/]*)$', self.name).group(1)

    def __repr__(self):
        return """
{}(
script: {},
  exec: {},
   cmd: {}
)
""".format(self.shortname(), self.command, self.name, self.args, self.concat_callable())

