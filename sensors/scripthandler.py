#!/usr/bin/env python3

import re
import subprocess
import sys

class Script:
    def __init__(self, name, args, command='python'):
        if not file_exists(name):
            raise ValueError('File not found! (did you provide the full path?)')
        self.name    = name
        self.args    = args
        self.command = command

    def call(self):
        '''Runs the script and returns a tuple of its stdout and return value.'''
        try:
            # Source: https://code-maven.com/python-capture-stdout-stderr-exit
            cmd = [self.command, script]
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE)
            stdout = str(proc.communicate()[0])[2:-3]
            return stdout, proc.returncode
        except Exception as exception:
            errorstr = 'E: scripthandler.py: call(): Exception occurred for \'{}\': \'{}\'. Reading failed.'.format(cmd, type(exception).__name__)
            print(errorstr)
            return tuple(errorstr, None)

    def concat_callable(self):
        '''Returns a string which, if run, will execute the script (similar to call(), but doesn't execute anything)'''
        return '{} {} {}'.format(self.command, self.name, self.args)

    def shortname(self):
        '''Extracts the script filename from its full path and returns it.'''
        return re.search(r'/([^/]*)$', self.name).group(1)

    def __repr__(self):
        return """
{}(
script: {},
  exec: {},
   cmd: {}
)
""".format(self.shortname(), self.command, self.name, self.args, self.concat_callable())

def file_exists(path):
    try:
        f = open(path)
        f.close()
        return True
    except FileNotFoundError:
        return False

