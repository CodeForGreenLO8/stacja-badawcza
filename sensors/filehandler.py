#!/usr/bin/env python3

# ABOUT THIS MODULE
# This module provides a few basic methods for interacting with files.
# It is used by numerous other scripts and modules.

import os

def file_exists(path):
    try:
        f = open(path)
        f.close()
        return True
    except FileNotFoundError:
        return False

def file_delete(path):
    if file_exists(path):
        try:
            os.remove(path)
            return True
        except Exception as exception:
            print('E: Exception occurred: {}'.format(type(exception).__name__)
            return False
    else:
        print('W: The specified file doesn\'t exist!')
        return False
