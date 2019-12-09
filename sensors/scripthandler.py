#!/usr/bin/env python3

import re
import subprocess
import sys

class Script:
    def __init__(self, name, args, command='python'):
        self.name    = name
        self.args    = args
        self.command = command
        
    def call(self):
        try:
            # Source: https://code-maven.com/python-capture-stdout-stderr-exit
            cmd = [self.command, script]
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE)
            stdout = str(proc.communicate()[0])[2:-3]
            return stdout, proc.returncode
        except Exception as exception:
            errorstr = 'E: scripthandler.py: Exception occurred for \'{}\': \'{}\'. Reading failed.'.format(cmd, type(exception).__name__)
            print(errorstr)
            return tuple(errorstr, None)

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

