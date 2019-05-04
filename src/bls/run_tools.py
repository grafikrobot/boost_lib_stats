"""
    Copyright (C) 2018-2019 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from .git_tool import Git
from .util import Main, PushDir
import os
import os.path


class CloneBoost(Main):
    def __init_parser__(self, parser):
        parser.add_argument('++root')
        parser.add_argument('++branch')

    def __run__(self):
        git = Git(self.args)
        if not os.path.exists(self.args.root):
            if not os.path.exists(os.path.dirname(self.args.root)):
                os.makedirs(os.path.dirname(self.args.root))
            git.clone_all('https://github.com/boostorg/boost.git',
                          self.args.root)
        else:
            git.fetch_all(self.args.root)


class GitSwitch(Main):

    def __init_parser__(self, parser):
        parser.add_argument('++root')
        parser.add_argument('++branch')
        parser.add_argument('++tag')

    def __run__(self):
        git = Git(self.args)
        with PushDir(self.args.root):
            git.switch(branch=self.args.branch, tag=self.args.tag)
            git.status()
