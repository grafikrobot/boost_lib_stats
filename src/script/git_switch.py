#!/usr/bin/env python3
"""
    Copyright (C) 2018 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from bls.git_tool import Git
from bls.util import Main, PushDir


class GitSwitch(Main):

    def __init_parser__(self, parser):
        parser.add_argument('++root')
        parser.add_argument('++branch')

    def __run__(self):
        git = Git(self.args)
        with PushDir(self.args.root):
            git.switch(self.args.branch)
            git.status()

if __name__ == "__main__":
    GitSwitch()
