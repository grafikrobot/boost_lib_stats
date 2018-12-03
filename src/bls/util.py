"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import argparse
import os
import os.path
import re
from subprocess import check_call, call, check_output


class Commands():
    def __init__(self):
        self.args = argparse.Namespace()

    def __check_call__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return check_call(command)
        else:
            return None

    def __call__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return call(command)
        else:
            return None

    def __check_output__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return check_output(command)
        else:
            return ""

    def __re_search__(self, p, s, default=None):
        s = re.search(p, s)
        return s.group(1) if s else default


class Main(Commands):
    def __init__(self):
        parser = argparse.ArgumentParser(prefix_chars='+')
        # common args
        parser.add_argument('++debug', action='store_true')
        parser.add_argument('++trace', action='store_true')
        # subclass args
        self.__init_parser__(parser)
        # get the args
        self.args = parser.parse_args()
        # run the script
        self.__run__()

    def __init_parser__(self, parser):
        pass

    def __run__(self):
        pass


class PushDir():
    def __init__(self, *dirs):
        self.dir = os.path.abspath(os.path.join(*dirs))

    def __enter__(self):
        self.cwd = os.getcwd()
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        os.chdir(self.dir)
        return self.dir

    def __exit__(self, type, value, traceback):
        os.chdir(self.cwd)
